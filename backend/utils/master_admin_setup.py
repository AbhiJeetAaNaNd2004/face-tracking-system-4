"""
Master Admin Setup Utility

This module handles the creation of the Master Admin account during system initialization.
It ensures only one Master Admin exists and provides secure password generation.
"""

import secrets
import string
from typing import Tuple, Optional
from utils.security import hash_password, get_db_manager
from utils.logging import get_logger

logger = get_logger(__name__)

def generate_master_admin_password(length: int = 16) -> str:
    """
    Generate a secure password for the Master Admin account.
    
    Args:
        length: Length of the password (default: 16)
        
    Returns:
        Generated password string
    """
    # Use a mix of uppercase, lowercase, digits, and special characters
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def create_master_admin(
    email: str = "admin@company.com",
    department: str = "IT Administration",
    phone_number: Optional[str] = None
) -> Tuple[bool, str, Optional[str]]:
    """
    Create the Master Admin account if it doesn't exist.
    
    Args:
        email: Master Admin email address
        department: Department for the Master Admin
        phone_number: Optional phone number
        
    Returns:
        Tuple of (success, message, password)
        - success: Boolean indicating if creation was successful
        - message: Status message
        - password: Plain text password (only returned on successful creation)
    """
    db = get_db_manager()
    
    try:
        # Check if Master Admin already exists
        existing_master = db.get_master_admin()
        if existing_master:
            logger.info("Master Admin already exists")
            return False, "Master Admin already exists", None
        
        # Check if any user with the email already exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            logger.error(f"User with email {email} already exists")
            return False, f"User with email {email} already exists", None
        
        # Generate secure password
        master_password = generate_master_admin_password()
        hashed_password = hash_password(master_password)
        
        # Create Master Admin account
        success = db.create_user(
            email=email,
            password_hash=hashed_password,
            designation="admin",
            department=department,
            phone_number=phone_number,
            is_master_admin=True
        )
        
        if success:
            logger.info(f"Master Admin created successfully with email: {email}")
            return True, "Master Admin created successfully", master_password
        else:
            logger.error("Failed to create Master Admin account")
            return False, "Failed to create Master Admin account", None
            
    except Exception as e:
        logger.error(f"Error creating Master Admin: {e}")
        return False, f"Error creating Master Admin: {str(e)}", None

def initialize_master_admin_if_needed() -> None:
    """
    Initialize Master Admin account if no users exist in the system.
    This function should be called during system startup.
    """
    db = get_db_manager()
    
    try:
        # Check if any users exist
        user_count = db.count_users()
        
        if user_count == 0:
            logger.info("No users found in system. Creating Master Admin account...")
            
            success, message, password = create_master_admin()
            
            if success and password:
                # Display credentials in console/logs for secure retrieval
                print("\n" + "="*60)
                print("🚀 MASTER ADMIN ACCOUNT CREATED")
                print("="*60)
                print(f"Email: admin@company.com")
                print(f"Password: {password}")
                print("="*60)
                print("⚠️  IMPORTANT: Save these credentials securely!")
                print("⚠️  This password will not be shown again!")
                print("="*60 + "\n")
                
                # Log the creation (without password)
                logger.info("Master Admin account created and credentials displayed")
            else:
                logger.error(f"Failed to create Master Admin: {message}")
                
        else:
            logger.info(f"System already has {user_count} user(s). Skipping Master Admin creation.")
            
    except Exception as e:
        logger.error(f"Error during Master Admin initialization: {e}")

def get_master_admin_info() -> Optional[dict]:
    """
    Get Master Admin account information (without password).
    
    Returns:
        Dictionary with Master Admin info or None if not found
    """
    db = get_db_manager()
    
    try:
        master_admin = db.get_master_admin()
        if master_admin:
            return {
                "id": master_admin.id,
                "email": master_admin.email,
                "department": master_admin.department,
                "phone_number": master_admin.phone_number,
                "created_at": master_admin.created_at.isoformat(),
                "status": master_admin.status
            }
        return None
        
    except Exception as e:
        logger.error(f"Error fetching Master Admin info: {e}")
        return None

def reset_master_admin_password() -> Tuple[bool, str, Optional[str]]:
    """
    Reset Master Admin password (emergency function).
    
    Returns:
        Tuple of (success, message, new_password)
    """
    db = get_db_manager()
    
    try:
        master_admin = db.get_master_admin()
        if not master_admin:
            return False, "Master Admin not found", None
        
        # Generate new password
        new_password = generate_master_admin_password()
        hashed_password = hash_password(new_password)
        
        # Update password in database
        success = db.update_user_password(master_admin.id, hashed_password)
        
        if success:
            logger.info("Master Admin password reset successfully")
            return True, "Master Admin password reset successfully", new_password
        else:
            logger.error("Failed to reset Master Admin password")
            return False, "Failed to reset Master Admin password", None
            
    except Exception as e:
        logger.error(f"Error resetting Master Admin password: {e}")
        return False, f"Error resetting Master Admin password: {str(e)}", None