#!/usr/bin/env python3
"""
Test script for the user management system
"""
import sys
import os
import requests
import json

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.user_service import UserService
from app.schemas.user_schemas import UserLogin, UserCreate, MasterAdminSetup
from db.db_config import get_db

def test_user_service():
    """Test the user service directly."""
    print("🧪 Testing User Service...")
    
    db = next(get_db())
    user_service = UserService(db)
    
    try:
        # Test 1: Check if master admin exists
        exists = user_service.is_master_admin_exists()
        print(f"✅ Master admin exists: {exists}")
        
        # Test 2: Try to authenticate master admin
        user = user_service.authenticate_user("admin@facetracking.com", "FaceTrack2024!")
        if user:
            print(f"✅ Master admin authentication successful: {user.email}")
            print(f"   - ID: {user.id}")
            print(f"   - Designation: {user.designation}")
            print(f"   - Department: {user.department}")
            print(f"   - Is Master Admin: {user.is_master_admin}")
        else:
            print("❌ Master admin authentication failed")
            
        # Test 3: Try to create a regular admin (should work for master admin)
        if user:
            try:
                admin_data = UserCreate(
                    email="regular.admin@company.com",
                    password="AdminPass123!",
                    designation="admin",
                    department="HR",
                    phone_number="+1234567891"
                )
                new_admin = user_service.create_user(admin_data, user)
                print(f"✅ Regular admin created: {new_admin.email}")
            except Exception as e:
                print(f"❌ Failed to create regular admin: {e}")
                
        # Test 4: Try to create an employee (should work for any admin)
        if user:
            try:
                employee_data = UserCreate(
                    email="employee@company.com",
                    password="EmpPass123!",
                    designation="employee",
                    department="Engineering",
                    phone_number="+1234567892"
                )
                new_employee = user_service.create_user(employee_data, user)
                print(f"✅ Employee created: {new_employee.email}")
            except Exception as e:
                print(f"❌ Failed to create employee: {e}")
                
        # Test 5: Get user statistics
        try:
            stats = user_service.get_user_stats(user)
            print(f"✅ User statistics: {stats}")
        except Exception as e:
            print(f"❌ Failed to get user statistics: {e}")
            
    except Exception as e:
        print(f"❌ Error in user service test: {e}")
    finally:
        db.close()

def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Check if master admin exists
    try:
        response = requests.get(f"{base_url}/users/check/master-admin-exists")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Master admin exists API: {data}")
        else:
            print(f"❌ Master admin check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return
    
    # Test 2: Login with master admin
    try:
        login_data = {
            "email": "admin@facetracking.com",
            "password": "FaceTrack2024!"
        }
        response = requests.post(f"{base_url}/users/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Master admin login successful")
            token = data["access_token"]
            print(f"   - Token: {token[:50]}...")
            
            # Test 3: Get current user info
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Current user info: {user_data['email']}")
            else:
                print(f"❌ Failed to get current user info: {response.status_code}")
                
            # Test 4: Get user statistics
            response = requests.get(f"{base_url}/users/stats", headers=headers)
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ User statistics: {stats}")
            else:
                print(f"❌ Failed to get user statistics: {response.status_code}")
                
        else:
            print(f"❌ Master admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

def main():
    """Main test function."""
    print("🔧 User Management System Test")
    print("=" * 50)
    
    # Test the service layer
    test_user_service()
    
    # Test the API layer
    test_api_endpoints()
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    main()