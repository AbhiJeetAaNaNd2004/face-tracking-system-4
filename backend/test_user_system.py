#!/usr/bin/env python3
"""
Simple test script to verify the user management system is working.
This script tests the core functionality without running the full FastAPI server.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.master_admin_setup import create_master_admin, get_master_admin_info
from utils.security import hash_password, verify_password, get_db_manager
from db.db_config import create_tables

def test_user_system():
    """Test the user management system components"""
    print("🧪 Testing User Management System")
    print("=" * 50)
    
    try:
        # Initialize database
        print("1. Initializing database...")
        create_tables()
        print("   ✅ Database tables created successfully")
        
        # Test password hashing
        print("\n2. Testing password security...")
        test_password = "TestPassword123!"
        hashed = hash_password(test_password)
        is_valid = verify_password(test_password, hashed)
        print(f"   ✅ Password hashing and verification: {'PASS' if is_valid else 'FAIL'}")
        
        # Test database manager
        print("\n3. Testing database manager...")
        db = get_db_manager()
        user_count = db.count_users()
        print(f"   ✅ Database connection successful. Current user count: {user_count}")
        
        # Test master admin creation
        print("\n4. Testing master admin creation...")
        if user_count == 0:
            success, message, password = create_master_admin()
            if success:
                print(f"   ✅ Master admin created successfully")
                print(f"   📧 Email: admin@company.com")
                print(f"   🔐 Password: {password}")
                print("   ⚠️  Save these credentials securely!")
            else:
                print(f"   ❌ Failed to create master admin: {message}")
        else:
            print("   ℹ️  Master admin already exists or users present")
        
        # Test master admin info retrieval
        print("\n5. Testing master admin info retrieval...")
        master_info = get_master_admin_info()
        if master_info:
            print(f"   ✅ Master admin found: {master_info['email']}")
            print(f"   📅 Created: {master_info['created_at']}")
            print(f"   🏢 Department: {master_info['department']}")
        else:
            print("   ❌ No master admin found")
        
        # Test user creation
        print("\n6. Testing user creation...")
        test_email = "test.employee@company.com"
        test_password_hash = hash_password("TempPassword123!")
        
        success = db.create_user(
            email=test_email,
            password_hash=test_password_hash,
            designation="employee",
            department="Testing",
            phone_number="+1234567890"
        )
        
        if success:
            print(f"   ✅ Test employee created: {test_email}")
            
            # Test user retrieval
            user = db.get_user_by_email(test_email)
            if user:
                print(f"   ✅ User retrieval successful: {user.designation}")
            else:
                print("   ❌ Failed to retrieve created user")
        else:
            print("   ⚠️  Test employee creation failed (might already exist)")
        
        print("\n" + "=" * 50)
        print("🎉 User Management System Test Complete!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_user_system()
    sys.exit(0 if success else 1)