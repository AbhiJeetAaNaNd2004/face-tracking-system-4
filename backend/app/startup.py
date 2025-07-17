"""
Startup script for the Face Tracking System.
Handles initial system setup including master admin creation.
"""
import os
import sys
from sqlalchemy.orm import Session

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_config import get_db, create_tables
from app.services.user_service import UserService
from app.schemas.user_schemas import MasterAdminSetup

def setup_master_admin_if_needed():
    """Set up master admin if it doesn't exist."""
    db = next(get_db())
    user_service = UserService(db)
    
    try:
        # Check if master admin already exists
        if user_service.is_master_admin_exists():
            print("✅ Master admin already exists. Skipping setup.")
            return
        
        print("🔧 No master admin found. Setting up master admin...")
        
        # Create master admin with default credentials
        master_admin_data = MasterAdminSetup(
            email="admin@company.com",
            password="TempPass123!",
            department="IT Administration",
            phone_number="+1234567890"
        )
        
        master_admin, plain_password = user_service.create_master_admin(master_admin_data)
        
        # Display credentials
        print("\n" + "=" * 70)
        print("🔐 MASTER ADMIN ACCOUNT CREATED SUCCESSFULLY")
        print("=" * 70)
        print(f"📧 Email: {master_admin.email}")
        print(f"🔑 Password: {plain_password}")
        print(f"🏢 Department: {master_admin.department}")
        print(f"📞 Phone: {master_admin.phone_number or 'Not provided'}")
        print("=" * 70)
        print("⚠️  IMPORTANT SECURITY NOTICE:")
        print("⚠️  1. Save these credentials securely!")
        print("⚠️  2. Change the password immediately after first login!")
        print("⚠️  3. This password will not be shown again!")
        print("⚠️  4. Use these credentials to access the admin panel!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error setting up master admin: {e}")
        raise
    finally:
        db.close()

def initialize_system():
    """Initialize the system with required setup."""
    try:
        print("🚀 Initializing Face Tracking System...")
        
        # Create database tables
        create_tables()
        print("✅ Database tables created/verified")
        
        # Setup master admin if needed
        setup_master_admin_if_needed()
        
        print("🎯 System initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        raise

if __name__ == "__main__":
    initialize_system()