from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta

from db.db_config import get_db
from app.services.user_service import UserService
from app.schemas.user_schemas import (
    UserCreate, UserResponse, UserLogin, UserUpdate, 
    PasswordChange, TokenResponse, UserListResponse,
    MasterAdminSetup
)
from app.dependencies.auth import (
    get_current_active_user, require_admin, require_master_admin,
    require_employee_or_admin
)
from db.db_models import User

router = APIRouter(prefix="/users", tags=["User Management"])

@router.post("/setup-master-admin", response_model=dict)
async def setup_master_admin(
    master_admin_data: MasterAdminSetup,
    db: Session = Depends(get_db)
):
    """
    Setup the master admin account (only if none exists).
    This endpoint is only available during initial system setup.
    """
    try:
        user_service = UserService(db)
        
        if user_service.is_master_admin_exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Master admin already exists"
            )
        
        master_admin, plain_password = user_service.create_master_admin(master_admin_data)
        
        # Log the credentials for secure retrieval (this is the only time the password is shown)
        print("=" * 60)
        print("🔐 MASTER ADMIN ACCOUNT CREATED")
        print("=" * 60)
        print(f"📧 Email: {master_admin.email}")
        print(f"🔑 Password: {plain_password}")
        print(f"🏢 Department: {master_admin.department}")
        print(f"📞 Phone: {master_admin.phone_number or 'Not provided'}")
        print("=" * 60)
        print("⚠️  IMPORTANT: Save these credentials securely!")
        print("⚠️  This password will not be shown again!")
        print("=" * 60)
        
        return {
            "message": "Master admin created successfully",
            "email": master_admin.email,
            "note": "Password has been displayed in the console logs. Please save it securely."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    try:
        user_service = UserService(db)
        user = user_service.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Update last login time
        user_service.update_last_login(user)
        
        # Create access token
        access_token = user_service.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return UserResponse.from_orm(current_user)

@router.post("/create", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new user (admin or employee based on role permissions)."""
    try:
        user_service = UserService(db)
        new_user = user_service.create_user(user_data, current_user)
        return UserResponse.from_orm(new_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get list of users with pagination (admin only)."""
    try:
        user_service = UserService(db)
        users, total = user_service.get_users(current_user, page, per_page)
        
        return UserListResponse(
            users=[UserResponse.from_orm(user) for user in users],
            total=total,
            page=page,
            per_page=per_page
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/stats", response_model=dict)
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get user statistics (admin only)."""
    try:
        user_service = UserService(db)
        stats = user_service.get_user_stats(current_user)
        return stats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get user by ID (admin only)."""
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user information."""
    try:
        user_service = UserService(db)
        updated_user = user_service.update_user(user_id, user_data, current_user)
        return UserResponse.from_orm(updated_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{user_id}/change-password")
async def change_user_password(
    user_id: int,
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Change user password."""
    try:
        user_service = UserService(db)
        success = user_service.change_password(user_id, password_data, current_user)
        
        if success:
            return {"message": "Password changed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete user (soft delete by deactivating)."""
    try:
        user_service = UserService(db)
        success = user_service.delete_user(user_id, current_user)
        
        if success:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete user"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/create-admin", response_model=UserResponse)
async def create_admin_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_master_admin)
):
    """Create a new admin user (master admin only)."""
    try:
        # Force designation to admin
        user_data.designation = "admin"
        
        user_service = UserService(db)
        new_admin = user_service.create_user(user_data, current_user)
        return UserResponse.from_orm(new_admin)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/create-employee", response_model=UserResponse)
async def create_employee_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new employee user (admin only)."""
    try:
        # Force designation to employee
        user_data.designation = "employee"
        
        user_service = UserService(db)
        new_employee = user_service.create_user(user_data, current_user)
        return UserResponse.from_orm(new_employee)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/check/master-admin-exists")
async def check_master_admin_exists(db: Session = Depends(get_db)):
    """Check if master admin exists (public endpoint for setup)."""
    user_service = UserService(db)
    exists = user_service.is_master_admin_exists()
    return {"master_admin_exists": exists}