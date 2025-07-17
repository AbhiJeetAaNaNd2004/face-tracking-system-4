# Employee & Admin Account Management System

## Overview

This system implements a comprehensive role-based user management system with proper security controls and access restrictions. The system supports three types of users: Master Admin, Regular Admin, and Employee accounts.

## System Architecture

### User Roles & Permissions

| Role | Can Create Admins? | Can Create Employees? | Special Privileges |
|------|-------------------|----------------------|-------------------|
| **Master Admin** | ✅ | ✅ | System-wide management |
| **Regular Admin** | ❌ | ✅ | User management only |
| **Employee** | ❌ | ❌ | Basic system access |

### Database Schema

The system uses a modified `users` table with the following structure:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    designation VARCHAR NOT NULL,  -- "employee" or "admin"
    department VARCHAR NOT NULL,
    phone_number VARCHAR,          -- Optional
    is_master_admin BOOLEAN DEFAULT FALSE,
    status VARCHAR DEFAULT 'active',
    last_login_time DATETIME,
    role_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication

#### POST `/auth/login/`
- **Purpose**: Authenticate user and return JWT token
- **Request Body**:
  ```json
  {
    "email": "user@company.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### User Management

#### POST `/user-management/enroll-employee`
- **Purpose**: Enroll a new employee or admin account
- **Access**: Admin or Master Admin
- **Request Body**:
  ```json
  {
    "email": "employee@company.com",
    "designation": "employee",  // "employee" or "admin"
    "department": "Engineering",
    "phone_number": "+1234567890"  // Optional
  }
  ```
- **Response**:
  ```json
  {
    "message": "Employee account created successfully",
    "user_id": 123,
    "email": "employee@company.com",
    "temporary_password": "TempPass123!"
  }
  ```

#### POST `/user-management/create-admin`
- **Purpose**: Create a new admin account
- **Access**: Master Admin only
- **Request Body**:
  ```json
  {
    "email": "admin@company.com",
    "department": "IT Administration",
    "phone_number": "+1234567890"  // Optional
  }
  ```

#### POST `/user-management/create-employee`
- **Purpose**: Create a new employee account
- **Access**: Admin or Master Admin
- **Request Body**:
  ```json
  {
    "email": "employee@company.com",
    "department": "Engineering",
    "phone_number": "+1234567890"  // Optional
  }
  ```

#### GET `/user-management/users`
- **Purpose**: List all users (optionally filtered by designation)
- **Access**: Admin or Master Admin
- **Query Parameters**: `designation` (optional): "employee" or "admin"
- **Response**:
  ```json
  [
    {
      "id": 1,
      "email": "user@company.com",
      "designation": "employee",
      "department": "Engineering",
      "phone_number": "+1234567890",
      "is_master_admin": false,
      "status": "active",
      "created_at": "2024-01-01T10:00:00"
    }
  ]
  ```

#### GET `/user-management/my-profile`
- **Purpose**: Get current user's profile information
- **Access**: Any authenticated user
- **Response**: User profile object

#### GET `/user-management/access-rights`
- **Purpose**: Get current user's access rights and permissions
- **Access**: Any authenticated user
- **Response**:
  ```json
  {
    "can_create_admins": false,
    "can_create_employees": true,
    "can_view_users": true,
    "can_manage_system": false,
    "designation": "admin",
    "is_master_admin": false
  }
  ```

## Master Admin Initialization

### Automatic Setup

When the system starts for the first time (no users exist), it automatically:

1. Creates a Master Admin account
2. Generates a secure random password
3. Displays the credentials **once** in the console:

```
============================================================
🚀 MASTER ADMIN ACCOUNT CREATED
============================================================
Email: admin@company.com
Password: Xy9#mK2$vL8@nR4!
============================================================
⚠️  IMPORTANT: Save these credentials securely!
⚠️  This password will not be shown again!
============================================================
```

### Manual Master Admin Creation

You can also create a Master Admin manually using the utility function:

```python
from utils.master_admin_setup import create_master_admin

success, message, password = create_master_admin(
    email="admin@company.com",
    department="IT Administration",
    phone_number="+1234567890"
)

if success:
    print(f"Master Admin created with password: {password}")
```

## Security Features

### Password Security
- All passwords are hashed using bcrypt
- Temporary passwords are generated with secure random characters
- Passwords are never stored in plain text after initial creation

### Access Control
- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting on login attempts
- Token expiration and validation

### Audit Logging
- All user creation events are logged
- Authentication attempts are tracked
- Status changes are recorded

## Usage Examples

### Creating Users Programmatically

```python
from utils.security import hash_password, get_db_manager

# Create an employee
db = get_db_manager()
success = db.create_user(
    email="employee@company.com",
    password_hash=hash_password("temporary_password"),
    designation="employee",
    department="Engineering",
    phone_number="+1234567890"
)

# Create an admin (only if current user is master admin)
success = db.create_user(
    email="admin@company.com",
    password_hash=hash_password("temporary_password"),
    designation="admin",
    department="IT Administration",
    is_master_admin=False
)
```

### Checking User Permissions

```python
from utils.security import verify_token, require_master_admin

# In your endpoint
@router.post("/admin-only-endpoint")
def admin_endpoint(current_user: dict = Depends(require_master_admin)):
    # Only master admin can access this
    return {"message": "Master admin access granted"}
```

## Error Handling

The system provides comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid credentials or expired token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: User not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side errors

## Configuration

### Environment Variables

```env
# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=sqlite:///face_tracking.db
```

## Migration Guide

If you're upgrading from the old system:

1. **Database Migration**: The `users` table structure has changed from `username` to `email`
2. **API Changes**: Login endpoint now expects `email` instead of `username`
3. **Token Structure**: JWT tokens now contain additional user information
4. **Role System**: New role-based access control replaces simple admin/user roles

## Testing

### Unit Tests

```python
def test_create_master_admin():
    success, message, password = create_master_admin()
    assert success == True
    assert password is not None
    assert len(password) >= 16

def test_role_based_access():
    # Test that only master admin can create admin accounts
    # Test that admin can create employee accounts
    # Test that employee cannot create any accounts
```

### Integration Tests

```python
def test_user_creation_flow():
    # Login as master admin
    # Create admin account
    # Login as admin
    # Create employee account
    # Verify permissions
```

## Best Practices

1. **Password Management**: Always use temporary passwords and force users to change them
2. **Access Control**: Follow the principle of least privilege
3. **Audit Logging**: Monitor all user management activities
4. **Error Handling**: Provide meaningful error messages without exposing sensitive information
5. **Rate Limiting**: Implement proper rate limiting to prevent brute force attacks

## Troubleshooting

### Common Issues

1. **Master Admin Not Created**: Check if users already exist in the database
2. **Permission Denied**: Verify user roles and token validity
3. **Database Connection**: Ensure database is properly configured
4. **Token Expiration**: Check token expiration settings

### Debug Commands

```python
# Check if master admin exists
from utils.master_admin_setup import get_master_admin_info
master_info = get_master_admin_info()
print(master_info)

# Count users in system
from utils.security import get_db_manager
db = get_db_manager()
user_count = db.count_users()
print(f"Total users: {user_count}")
```

## Support

For issues or questions regarding the user management system:

1. Check the logs for error messages
2. Verify database connectivity
3. Ensure proper environment configuration
4. Review API documentation for correct usage