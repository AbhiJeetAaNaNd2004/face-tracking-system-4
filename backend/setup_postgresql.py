#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script for Face Tracking System
=========================================================

This script helps set up the PostgreSQL database for the Face Tracking System.
It creates the database, user, and necessary permissions.

Usage:
    python setup_postgresql.py

Requirements:
    - PostgreSQL server running
    - psycopg2 package installed
    - Superuser access to PostgreSQL
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_postgresql_running():
    """Check if PostgreSQL service is running."""
    try:
        # Try to connect to PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres'  # Default password
        )
        conn.close()
        return True
    except Exception:
        return False

def create_database():
    """Create the face_tracking database and user."""
    try:
        # Connect to PostgreSQL as superuser
        print("🔌 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password=input("Enter PostgreSQL superuser password: ")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database
        print("📊 Creating database 'face_tracking'...")
        try:
            cursor.execute("CREATE DATABASE face_tracking;")
            print("✅ Database 'face_tracking' created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print("ℹ️  Database 'face_tracking' already exists")
        
        # Create user (if not exists)
        print("👤 Creating user 'postgres' with password...")
        try:
            cursor.execute("CREATE USER postgres WITH ENCRYPTED PASSWORD 'password';")
            print("✅ User 'postgres' created successfully")
        except psycopg2.errors.DuplicateObject:
            print("ℹ️  User 'postgres' already exists")
        
        # Grant privileges
        print("🔐 Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE face_tracking TO postgres;")
        cursor.execute("ALTER USER postgres CREATEDB;")
        print("✅ Privileges granted successfully")
        
        cursor.close()
        conn.close()
        
        print("\n🎯 Database setup completed successfully!")
        print("📋 Database Configuration:")
        print("   - Host: localhost")
        print("   - Port: 5432")
        print("   - Database: face_tracking")
        print("   - User: postgres")
        print("   - Password: password")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

def test_connection():
    """Test connection to the created database."""
    try:
        print("\n🧪 Testing database connection...")
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='face_tracking',
            user='postgres',
            password='password'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connection successful! PostgreSQL version: {version}")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        sys.exit(1)

def install_requirements():
    """Install required Python packages."""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
        print("✅ psycopg2-binary installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install psycopg2-binary: {e}")
        sys.exit(1)

def main():
    """Main setup function."""
    print("🐘 PostgreSQL Database Setup for Face Tracking System")
    print("=" * 55)
    
    # Check if PostgreSQL is running
    if not check_postgresql_running():
        print("❌ PostgreSQL is not running or not accessible")
        print("Please ensure PostgreSQL is installed and running")
        print("\nUbuntu/Debian:")
        print("  sudo apt update")
        print("  sudo apt install postgresql postgresql-contrib")
        print("  sudo systemctl start postgresql")
        print("\nCentOS/RHEL:")
        print("  sudo yum install postgresql-server postgresql-contrib")
        print("  sudo postgresql-setup initdb")
        print("  sudo systemctl start postgresql")
        print("\nmacOS:")
        print("  brew install postgresql")
        print("  brew services start postgresql")
        print("\nWindows:")
        print("  Download and install from https://www.postgresql.org/download/windows/")
        sys.exit(1)
    
    # Install requirements
    install_requirements()
    
    # Create database
    create_database()
    
    # Test connection
    test_connection()
    
    print("\n🚀 Setup completed! You can now start the Face Tracking System.")
    print("💡 Next steps:")
    print("   1. cd backend")
    print("   2. source venv/bin/activate")
    print("   3. python3 start.py")

if __name__ == "__main__":
    main()