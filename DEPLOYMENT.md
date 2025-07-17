# 🚀 Deployment Guide - Face Tracking System

This guide provides comprehensive instructions for deploying the Face Tracking System in various environments.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 20GB available space
- **Network**: Internet connection for initial setup

### Software Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **PostgreSQL**: 12.x or higher
- **Docker**: 20.x or higher (optional but recommended)
- **Git**: Latest version

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker
```bash
# Clone the repository
git clone https://github.com/your-org/face-tracking-system-7.git
cd face-tracking-system-7

# Start the database
docker-compose up -d postgres

# Wait for database to be ready
docker-compose logs -f postgres

# Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend
python3 start.py

# In another terminal, set up frontend
cd frontend
npm install
npm run dev
```

### Full Docker Setup
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Services
- **PostgreSQL**: `localhost:5432`
- **pgAdmin**: `localhost:5050`

## 🔧 Manual Deployment

### 1. Database Setup

#### Ubuntu/Debian
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE face_tracking;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE face_tracking TO postgres;
\q
```

#### CentOS/RHEL
```bash
# Install PostgreSQL
sudo yum install postgresql-server postgresql-contrib

# Initialize database
sudo postgresql-setup initdb

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Configure authentication (edit /var/lib/pgsql/data/pg_hba.conf)
sudo vi /var/lib/pgsql/data/pg_hba.conf
# Change 'ident' to 'md5' for local connections

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### macOS
```bash
# Install PostgreSQL using Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb face_tracking
```

### 2. Backend Deployment

```bash
# Clone repository
git clone https://github.com/your-org/face-tracking-system-7.git
cd face-tracking-system-7/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database setup (if needed)
python3 setup_postgresql.py

# Start the server
python3 start.py --host 0.0.0.0 --port 8000
```

### 3. Frontend Deployment

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve with a static server (optional)
npm install -g serve
serve -s dist -l 3000
```

## 🌐 Production Deployment

### Backend Production Setup

#### Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn configuration
cat > gunicorn.conf.py << EOF
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
EOF

# Start with Gunicorn
gunicorn -c gunicorn.conf.py app.main:app
```

#### Using Systemd Service
```bash
# Create systemd service file
sudo tee /etc/systemd/system/face-tracking-backend.service << EOF
[Unit]
Description=Face Tracking System Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/face-tracking-system-7/backend
Environment=PATH=/path/to/face-tracking-system-7/backend/venv/bin
ExecStart=/path/to/face-tracking-system-7/backend/venv/bin/python start.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable face-tracking-backend
sudo systemctl start face-tracking-backend
```

### Frontend Production Setup

#### Using Nginx
```bash
# Install Nginx
sudo apt install nginx

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/face-tracking << EOF
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/face-tracking-system-7/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/face-tracking /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Configuration with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔐 Security Configuration

### Environment Variables
```env
# Production environment variables
DATABASE_URL=postgresql://user:secure_password@localhost:5432/face_tracking
SECRET_KEY=your-super-secret-key-here
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=WARNING
ALLOWED_ORIGINS=https://your-domain.com
```

### Database Security
```sql
-- Create dedicated database user
CREATE USER face_tracking_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE face_tracking TO face_tracking_user;
GRANT USAGE ON SCHEMA public TO face_tracking_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO face_tracking_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO face_tracking_user;
```

### Firewall Configuration
```bash
# Ubuntu/Debian
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp  # PostgreSQL (restrict to localhost in production)
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload
```

## 📊 Monitoring and Logging

### Application Monitoring
```bash
# Install monitoring tools
pip install prometheus-client
pip install grafana-api

# Set up log rotation
sudo tee /etc/logrotate.d/face-tracking << EOF
/var/log/face-tracking/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
}
EOF
```

### Health Checks
```bash
# Backend health check
curl -f http://localhost:8000/health || exit 1

# Database health check
pg_isready -h localhost -p 5432 -U postgres
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Create backup script
cat > backup_db.sh << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/face-tracking"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Create database backup
pg_dump -h localhost -U postgres face_tracking > $BACKUP_DIR/face_tracking_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
EOF

chmod +x backup_db.sh

# Add to crontab for daily backups
echo "0 2 * * * /path/to/backup_db.sh" | crontab -
```

### Recovery Process
```bash
# Restore from backup
psql -h localhost -U postgres -d face_tracking < /var/backups/face-tracking/face_tracking_YYYYMMDD_HHMMSS.sql
```

## 🚀 Scaling and Performance

### Load Balancing
```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

### Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_attendance_timestamp ON attendance_records(timestamp);
CREATE INDEX idx_attendance_employee_id ON attendance_records(employee_id);
```

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connectivity
psql -h localhost -U postgres -d face_tracking

# Check logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### Application Errors
```bash
# Check application logs
tail -f /var/log/face-tracking/app.log

# Check system resources
htop
df -h
```

### Performance Issues
```bash
# Monitor database performance
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_database;

# Check slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify system requirements
4. Check network connectivity
5. Consult the documentation

## 🎯 Deployment Checklist

### Pre-deployment
- [ ] System requirements met
- [ ] Database configured
- [ ] SSL certificates obtained
- [ ] Firewall configured
- [ ] Backup system in place

### Deployment
- [ ] Code deployed
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Database migrations run
- [ ] Services started

### Post-deployment
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Logs accessible
- [ ] Backup tested
- [ ] Performance verified

---

**🎉 Congratulations! Your Face Tracking System is now deployed and ready for use.**