# Contributing to Employee Monitoring System

Thank you for your interest in contributing to the Employee Monitoring System! This document provides guidelines and instructions for contributing to the project.

## 🤝 How to Contribute

### 1. Fork the Repository
- Fork the repository to your GitHub account
- Clone your fork locally:
```bash
git clone https://github.com/your-username/employee-monitoring-system.git
cd employee-monitoring-system
```

### 2. Set Up Development Environment

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Write clean, readable code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Backend tests
cd backend
python3 test_user_system.py

# Frontend tests
cd frontend
npm run test  # If tests are available
```

### 6. Commit Your Changes
```bash
git add .
git commit -m "Add: Brief description of your changes"
```

### 7. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
- Go to GitHub and create a pull request
- Fill out the pull request template
- Wait for review and feedback

## 📋 Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use meaningful variable and function names

Example:
```python
def create_user(user_data: UserCreate, current_user: User) -> User:
    """
    Create a new user with role-based access control.
    
    Args:
        user_data: User creation data
        current_user: User performing the action
        
    Returns:
        Created user object
        
    Raises:
        ValueError: If user creation fails
    """
    # Implementation here
```

#### JavaScript/Vue.js (Frontend)
- Use ES6+ features
- Follow Vue.js style guide
- Use meaningful component and variable names
- Add comments for complex logic

Example:
```javascript
/**
 * Authenticate user and redirect to appropriate dashboard
 * @param {Object} credentials - User login credentials
 */
async function login(credentials) {
  // Implementation here
}
```

### Git Commit Messages
Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or modifications
- `chore:` - Maintenance tasks

Examples:
- `feat: add user profile management`
- `fix: resolve authentication token expiration`
- `docs: update API documentation`

### Testing
- Write unit tests for new functions
- Test edge cases and error conditions
- Ensure all existing tests pass
- Add integration tests for new features

### Documentation
- Update README.md if needed
- Add inline code comments
- Update API documentation
- Create or update user guides

## 🐛 Bug Reports

When reporting bugs, please include:
- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, Node.js version, browser
- **Screenshots**: If applicable

## 💡 Feature Requests

When suggesting features, please include:
- **Use Case**: Why this feature would be useful
- **Description**: Detailed description of the feature
- **Implementation Ideas**: If you have ideas on how to implement it
- **Alternatives**: Alternative solutions you've considered

## 🔒 Security

If you discover a security vulnerability, please:
- **Do not** create a public issue
- Email the maintainers directly
- Provide detailed information about the vulnerability
- Allow time for the issue to be addressed before disclosure

## 📝 Pull Request Guidelines

### Before Submitting
- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] Branch is up to date with main

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

## 🏗️ Project Structure

### Backend (`backend/`)
- `app/` - Main application code
  - `dependencies/` - Authentication and authorization
  - `routers/` - API endpoints
  - `schemas/` - Pydantic models
  - `services/` - Business logic
- `db/` - Database models and configuration
- `utils/` - Utility functions
- `tasks/` - Background tasks

### Frontend (`frontend/`)
- `src/` - Source code
  - `components/` - Vue.js components
  - `router/` - Vue Router configuration
  - `style.css` - Global styles

## 🚀 Development Workflow

1. **Issue Creation**: Create or find an issue to work on
2. **Branch Creation**: Create a feature branch
3. **Development**: Implement your changes
4. **Testing**: Test your changes thoroughly
5. **Documentation**: Update relevant documentation
6. **Pull Request**: Submit for review
7. **Review**: Address feedback and make changes
8. **Merge**: Once approved, changes are merged

## 📞 Getting Help

If you need help:
- Check existing issues and documentation
- Ask questions in discussions
- Contact maintainers
- Join our community chat (if available)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the Employee Monitoring System! 🎉