from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import secrets
import string

from utils.security import (
    verify_token,
    require_master_admin,
    require_admin_or_master,
    can_create_admin,
    can_create_employee,
    get_db_manager,
    hash_password
)
from utils.logging import get_logger

logger = get_logger(__name__)

# FastAPI router
router = APIRouter(prefix="/user-management", tags=["User Management"])

# Pydantic Schemas
class EmployeeEnrollmentRequest(BaseModel):
    email: EmailStr
    designation: str  # "employee" or "admin"
    department: str
    phone_number: Optional[str] = None

class CreateAdminRequest(BaseModel):
    email: EmailStr
    department: str
    phone_number: Optional[str] = None

class CreateEmployeeRequest(BaseModel):
    email: EmailStr
    department: str
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    designation: str
    department: str
    phone_number: Optional[str]
    is_master_admin: bool
    status: str
    created_at: str

class MessageResponse(BaseModel):
    message: str
    user_id: Optional[int] = None
    email: Optional[str] = None
    temporary_password: Optional[str] = None

def generate_temporary_password(length: int = 12) -> str:
    """Generate a secure temporary password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# API Endpoints

@router.post("/enroll-employee", response_model=MessageResponse)
def enroll_employee(
    request: EmployeeEnrollmentRequest,
    current_user: dict = Depends(can_create_employee),
    db = Depends(get_db_manager)
):
    """
    Enroll a new employee account.
    Can be called by admin or master admin.
    """
    try:
        # Validate designation
        if request.designation not in ["employee", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Designation must be either 'employee' or 'admin'"
            )
        
        # Only master admin can create admin accounts
        if request.designation == "admin" and not current_user.get("is_master_admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Master Admin can create admin accounts"
            )
        
        # Generate temporary password
        temp_password = generate_temporary_password()
        hashed_password = hash_password(temp_password)
        
        # Create user
        success = db.create_user(
            email=request.email,
            password_hash=hashed_password,
            designation=request.designation,
            department=request.department,
            phone_number=request.phone_number,
            is_master_admin=False
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed. Email might already exist."
            )
        
        # Get the created user to return the ID
        created_user = db.get_user_by_email(request.email)
        
        logger.info(f"{request.designation.title()} {request.email} created by {current_user.get('email')}")
        
        return MessageResponse(
            message=f"{request.designation.title()} account created successfully",
            user_id=created_user.id if created_user else None,
            email=request.email,
            temporary_password=temp_password  # Return this once for secure retrieval
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enrolling employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/create-admin", response_model=MessageResponse)
def create_admin_account(
    request: CreateAdminRequest,
    current_user: dict = Depends(require_master_admin),
    db = Depends(get_db_manager)
):
    """
    Create a new admin account.
    Only master admin can create admin accounts.
    """
    try:
        # Generate temporary password
        temp_password = generate_temporary_password()
        hashed_password = hash_password(temp_password)
        
        # Create admin user
        success = db.create_user(
            email=request.email,
            password_hash=hashed_password,
            designation="admin",
            department=request.department,
            phone_number=request.phone_number,
            is_master_admin=False
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin creation failed. Email might already exist."
            )
        
        # Get the created user to return the ID
        created_user = db.get_user_by_email(request.email)
        
        logger.info(f"Admin {request.email} created by Master Admin {current_user.get('email')}")
        
        return MessageResponse(
            message="Admin account created successfully",
            user_id=created_user.id if created_user else None,
            email=request.email,
            temporary_password=temp_password  # Return this once for secure retrieval
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/create-employee", response_model=MessageResponse)
def create_employee_account(
    request: CreateEmployeeRequest,
    current_user: dict = Depends(can_create_employee),
    db = Depends(get_db_manager)
):
    """
    Create a new employee account.
    Can be called by admin or master admin.
    """
    try:
        # Generate temporary password
        temp_password = generate_temporary_password()
        hashed_password = hash_password(temp_password)
        
        # Create employee user
        success = db.create_user(
            email=request.email,
            password_hash=hashed_password,
            designation="employee",
            department=request.department,
            phone_number=request.phone_number,
            is_master_admin=False
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee creation failed. Email might already exist."
            )
        
        # Get the created user to return the ID
        created_user = db.get_user_by_email(request.email)
        
        logger.info(f"Employee {request.email} created by {current_user.get('email')}")
        
        return MessageResponse(
            message="Employee account created successfully",
            user_id=created_user.id if created_user else None,
            email=request.email,
            temporary_password=temp_password  # Return this once for secure retrieval
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/users", response_model=List[UserResponse])
def list_users(
    designation: Optional[str] = None,
    current_user: dict = Depends(require_admin_or_master),
    db = Depends(get_db_manager)
):
    """
    List all users, optionally filtered by designation.
    Available to admin and master admin.
    """
    try:
        if designation:
            if designation not in ["employee", "admin"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Designation must be either 'employee' or 'admin'"
                )
            users = db.get_users_by_designation(designation)
        else:
            # Get all users - this would need to be implemented in db_manager
            users = db.get_users_by_designation("employee") + db.get_users_by_designation("admin")
        
        return [
            UserResponse(
                id=user.id,
                email=user.email,
                designation=user.designation,
                department=user.department,
                phone_number=user.phone_number,
                is_master_admin=user.is_master_admin,
                status=user.status,
                created_at=user.created_at.isoformat()
            )
            for user in users
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/my-profile", response_model=UserResponse)
def get_my_profile(
    current_user: dict = Depends(verify_token),
    db = Depends(get_db_manager)
):
    """
    Get current user's profile information.
    """
    try:
        user = db.get_user_by_email(current_user.get("email"))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            designation=user.designation,
            department=user.department,
            phone_number=user.phone_number,
            is_master_admin=user.is_master_admin,
            status=user.status,
            created_at=user.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/access-rights")
def get_access_rights(current_user: dict = Depends(verify_token)):
    """
    Get current user's access rights and permissions.
    """
    designation = current_user.get("designation")
    is_master_admin = current_user.get("is_master_admin")
    
    rights = {
        "can_create_admins": is_master_admin,
        "can_create_employees": designation == "admin" or is_master_admin,
        "can_view_users": designation == "admin" or is_master_admin,
        "can_manage_system": is_master_admin,
        "designation": designation,
        "is_master_admin": is_master_admin
    }
    
    return rights