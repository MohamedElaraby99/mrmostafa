import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tafra-student-system-2025-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Railway/Heroku provides PostgreSQL URL, handle protocol properly
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///students.db'
    
    # Application settings
    APP_NAME = os.environ.get('APP_NAME', 'نظام الإدارة')
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Production optimizations
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///students.db'

class ProductionConfig(Config):
    """Production configuration for PythonAnywhere"""
    FLASK_ENV = 'production'
    DEBUG = False
    
    # PythonAnywhere SQLite database path
    # Update this path according to your PythonAnywhere username
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////home/yourusername/mysite/tafra_system.db'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Additional production settings
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # SQLite optimizations for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'echo': False
    }

class PythonAnywhereConfig(Config):
    """Specific configuration for PythonAnywhere deployment"""
    FLASK_ENV = 'production'
    DEBUG = False
    
    # PythonAnywhere database path - change 'yourusername' to your actual username
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////home/tafrasystem/mysite/tafra_system.db'
    
    # Security settings
    SESSION_COOKIE_SECURE = True  # Set to True for HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance settings for shared hosting
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'echo': False,
        'pool_size': 10
    }
    
    # Additional settings
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Static files configuration
    STATIC_FOLDER = '/home/tafrasystem/mysite/static'
    TEMPLATES_FOLDER = '/home/tafrasystem/mysite/templates'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'pythonanywhere': PythonAnywhereConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 