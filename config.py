# Database configuration
DATABASE = {
    'NAME': 'mydatabase',         # Replace with your actual database name
    'USER': 'myuser',             # Replace with your actual database username
    'PASSWORD': 'mypassword',     # Replace with your actual password
    'HOST': 'db',                 # The name of your db service in Docker (for Docker Compose)
    'PORT': '5432',               # Default PostgreSQL port
}

# Secret Key for Django application
SECRET_KEY = 'django-insecure-be56_n*1aq-t9-*82ilxk@j!m&q#nrf)p(q++fwr178f$x)53n'

# Debug mode for development
DEBUG = True

# Allowed Hosts (can be set in production)
ALLOWED_HOSTS = []

# Other settings can be added as needed
