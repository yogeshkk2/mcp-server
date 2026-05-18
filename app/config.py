"""
Configuration Module for MCP Server

This module contains all configuration settings for the MCP server application,
including server parameters, connection settings, and other constants.

Author: Yogesh Kadiya
"""


class Config:
    """
    Configuration class containing all server settings and constants.
    
    This class can be extended with environment-specific configurations
    (e.g., Development, Production, Testing) by inheritance.
    """
    
    # Server Network Configuration
    HOST = '0.0.0.0'                   # Bind to all network interfaces
    PORT = 5000                         # Server port
    
    # Debug and Development Settings
    DEBUG = True                        # Enable debug mode for development
    
    # Connection Settings
    CONNECTION_TIMEOUT = 30             # Connection timeout in seconds
    MAX_CONNECTIONS = 5                 # Maximum concurrent connections
    
    # Additional Configuration Options
    # Uncomment and configure as needed for your deployment:
    
    # Database Settings (if using a database)
    # DATABASE_URL = 'postgresql://user:password@localhost/dbname'
    # DATABASE_POOL_SIZE = 10
    # DATABASE_ECHO = False
    
    # Logging Configuration
    # LOG_LEVEL = 'INFO'
    # LOG_FILE = 'server.log'
    
    # API Settings
    # API_TITLE = 'MCP Server API'
    # API_VERSION = '1.0.0'
    # CORS_ORIGINS = ['*']
    
    # Security Settings
    # SECRET_KEY = 'your-secret-key-here'
    # JWT_ALGORITHM = 'HS256'
    # JWT_EXPIRY = 3600


# Optional: Environment-specific configurations

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    MAX_CONNECTIONS = 100


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    PORT = 5001
    MAX_CONNECTIONS = 1
