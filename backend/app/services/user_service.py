from sqlalchemy.orm import Session
from sqlalchemy import and_
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import secrets
import string
import os

from db.db_models import User
from app.schemas.user_schemas import UserCreate, UserUpdate, PasswordChange, MasterAdminSetup
from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    def generate_random_password(self, length: int = 12) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    def is_master_admin_exists(self) -> bool:
        """Check if master admin already exists."""
        return self.db.query(User).filter(User.is_master_admin == True).first() is not None

    def create_master_admin(self, master_admin_data: MasterAdminSetup) -> tuple[User, str]:
        """Create the master admin account."""
        if self.is_master_admin_exists():
            raise ValueError("Master admin already exists")

        # Generate random password if not provided
        plain_password = master_admin_data.password
        
        # Create master admin user
        master_admin = User(
            email=master_admin_data.email,
            hashed_password=self.get_password_hash(plain_password),
            designation="admin",
            department=master_admin_data.department,
            phone_number=master_admin_data.phone_number,
            is_master_admin=True,
            is_active=True,
            created_by=None  # Master admin is not created by anyone
        )
        
        self.db.add(master_admin)
        self.db.commit()
        self.db.refresh(master_admin)
        
        return master_admin, plain_password

    def can_create_admin(self, current_user: User) -> bool:
        """Check if current user can create admin accounts."""
        return current_user.is_master_admin

    def can_create_employee(self, current_user: User) -> bool:
        """Check if current user can create employee accounts."""
        return current_user.designation == "admin"

    def create_user(self, user_data: UserCreate, current_user: User) -> User:
        """Create a new user with role-based access control."""
        # Check if user already exists
        if self.get_user_by_email(user_data.email):
            raise ValueError("User with this email already exists")

        # Role-based access control
        if user_data.designation == "admin":
            if not self.can_create_admin(current_user):
                raise ValueError("Only Master Admin can create admin accounts")
        elif user_data.designation == "employee":
            if not self.can_create_employee(current_user):
                raise ValueError("Only admins can create employee accounts")

        # Create new user
        new_user = User(
            email=user_data.email,
            hashed_password=self.get_password_hash(user_data.password),
            designation=user_data.designation,
            department=user_data.department,
            phone_number=user_data.phone_number,
            is_master_admin=False,
            is_active=True,
            created_by=current_user.id
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user

    def update_user(self, user_id: int, user_data: UserUpdate, current_user: User) -> User:
        """Update user information."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Only allow users to update their own profile or admins to update others
        if user.id != current_user.id and current_user.designation != "admin":
            raise ValueError("Permission denied")

        # Update user fields
        if user_data.email is not None:
            # Check if email is already taken
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already taken")
            user.email = user_data.email

        if user_data.department is not None:
            user.department = user_data.department

        if user_data.phone_number is not None:
            user.phone_number = user_data.phone_number

        if user_data.is_active is not None and current_user.designation == "admin":
            user.is_active = user_data.is_active

        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user

    def change_password(self, user_id: int, password_data: PasswordChange, current_user: User) -> bool:
        """Change user password."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Only allow users to change their own password
        if user.id != current_user.id:
            raise ValueError("Permission denied")

        # Verify current password
        if not self.verify_password(password_data.current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")

        # Update password
        user.hashed_password = self.get_password_hash(password_data.new_password)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def delete_user(self, user_id: int, current_user: User) -> bool:
        """Delete user (soft delete by deactivating)."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Only admins can delete users
        if current_user.designation != "admin":
            raise ValueError("Permission denied")

        # Cannot delete master admin
        if user.is_master_admin:
            raise ValueError("Cannot delete master admin")

        # Soft delete by deactivating
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def get_users(self, current_user: User, page: int = 1, per_page: int = 10) -> tuple[List[User], int]:
        """Get list of users with pagination."""
        # Only admins can view all users
        if current_user.designation != "admin":
            raise ValueError("Permission denied")

        query = self.db.query(User).filter(User.is_active == True)
        
        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return users, total

    def update_last_login(self, user: User):
        """Update user's last login time."""
        user.last_login_time = datetime.utcnow()
        self.db.commit()

    def get_user_stats(self, current_user: User) -> dict:
        """Get user statistics."""
        if current_user.designation != "admin":
            raise ValueError("Permission denied")

        total_users = self.db.query(User).filter(User.is_active == True).count()
        total_admins = self.db.query(User).filter(
            and_(User.designation == "admin", User.is_active == True)
        ).count()
        total_employees = self.db.query(User).filter(
            and_(User.designation == "employee", User.is_active == True)
        ).count()

        return {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_employees": total_employees,
            "master_admin_exists": self.is_master_admin_exists()
        }