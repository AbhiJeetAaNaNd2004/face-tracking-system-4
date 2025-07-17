# 🔐 Employee Monitoring System

A comprehensive employee monitoring and management system with role-based access control, face recognition capabilities, and modern web interface.

## 🌟 Features

### 🔐 User Management
- **Role-based access control** (Master Admin, Regular Admin, Employee)
- **Secure authentication** with JWT tokens
- **Password hashing** with bcrypt
- **Automatic master admin setup**
- **User enrollment and management**

### 📊 Employee Dashboard
- **Personal attendance records**
- **Face embeddings (read-only)**
- **Employee status overview**
- **Modern, responsive UI**

### 🛠️ Admin Dashboard
- **Live camera feeds**
- **Employee management** (add, edit, delete)
- **Attendance logs**
- **System logs and monitoring**
- **User statistics**

### 🎯 Technical Features
- **FastAPI backend** with async support
- **Vue.js frontend** with modern UI
- **SQLite database** (easily configurable)
- **Real-time updates**
- **Comprehensive API documentation**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd employee-monitoring-system

# Set up Python virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python3 start.py
```

### Frontend Setup
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔑 Default Credentials

### Master Admin (Auto-created)
```
📧 Email: admin@company.com
🔑 Password: TempPass123!
```

> ⚠️ **Important**: Change the default password immediately after first login!

## 📁 Project Structure

```
employee-monitoring-system/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── dependencies/       # Authentication dependencies
│   │   ├── routers/           # API endpoints
│   │   ├── schemas/           # Pydantic models
│   │   ├── services/          # Business logic
│   │   └── main.py            # FastAPI app
│   ├── db/                    # Database models and config
│   ├── utils/                 # Utility functions
│   ├── tasks/                 # Background tasks
│   ├── requirements.txt       # Python dependencies
│   └── start.py              # Server startup script
├── frontend/                  # Vue.js frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── router/           # Vue router
│   │   └── style.css         # Global styles
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
└── docs/                     # Documentation
```

## 🔐 User Roles & Permissions

| Role | Can Create Admins? | Can Create Employees? | Dashboard Access |
|------|-------------------|----------------------|------------------|
| **Master Admin** | ✅ Yes | ✅ Yes | Full Admin Dashboard |
| **Regular Admin** | ❌ No | ✅ Yes | Admin Dashboard |
| **Employee** | ❌ No | ❌ No | Employee Dashboard |

## 🛠️ API Endpoints

### Authentication
- `POST /users/login` - User login
- `GET /users/me` - Get current user info
- `POST /users/setup-master-admin` - Setup master admin

### User Management (Admin Only)
- `GET /users/` - List all users
- `POST /users/create` - Create new user
- `POST /users/create-admin` - Create admin (master admin only)
- `POST /users/create-employee` - Create employee
- `GET /users/stats` - User statistics
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Employee Management
- `GET /employees/` - List employees
- `POST /employees/` - Create employee
- `GET /employees/{id}` - Get employee details

### Attendance
- `GET /attendance/` - Get attendance records
- `POST /attendance/` - Create attendance record

## 🔒 Security Features

### ✅ Implemented
- **Password hashing** with bcrypt
- **JWT authentication** with 30-minute expiration
- **Role-based access control**
- **Input validation** and sanitization
- **Secure password requirements** (min 8 characters)
- **One-time password display** for master admin
- **Audit trail** with user creation tracking

### 🛡️ Database Security
- **No plain text passwords**
- **Unique email constraints**
- **Soft delete** for user deactivation
- **Timestamp tracking** for auditing

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python3 test_user_system.py
```

### Test Results
```
✅ Master admin exists: True
✅ Master admin authentication successful
✅ Regular admin created successfully
✅ Employee created successfully
✅ User statistics working correctly
```

## 📖 Documentation

- [User Management System](USER_MANAGEMENT_SYSTEM.md) - Detailed documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Frontend Components](frontend/src/components/) - Vue.js components

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=sqlite:///face_tracking.db
SECRET_KEY=your-secret-key-here
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=INFO
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Database Configuration
The system uses SQLite by default. To use PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🚀 Deployment

### Backend Deployment
```bash
# Production startup
python3 start.py --host 0.0.0.0 --port 8000

# With multiple workers
python3 start.py --workers 4
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [documentation](docs/)
- Review the [API documentation](http://localhost:8000/docs)
- Open an issue on GitHub

## 🎯 System Status

- **Backend**: ✅ Fully Operational
- **Frontend**: ✅ Fully Operational
- **User Management**: ✅ Complete
- **Authentication**: ✅ Secure
- **Database**: ✅ Configured
- **API**: ✅ Documented

---

**Built with ❤️ using FastAPI, Vue.js, and modern web technologies**