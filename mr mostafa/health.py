"""
Health check endpoint for monitoring
"""
from flask import Blueprint, jsonify
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@health_bp.route('/ping')
def ping():
    """Simple ping endpoint"""
    return 'pong', 200

@health_bp.route('/status')
def status():
    """Detailed status information"""
    return jsonify({
        'app_name': 'Tafra Student Management System',
        'version': '1.0.0',
        'status': 'running',
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': 'healthy'
    }), 200 