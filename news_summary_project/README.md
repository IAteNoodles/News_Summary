# News Summary Project Module

This module contains the core Django project configuration and settings for the News Summary API. It serves as the central configuration hub that orchestrates all applications and services.

## Module Structure

```
news_summary_project/
├── __init__.py              # Package initialization
├── settings.py              # Django project settings
├── urls.py                  # Root URL configuration
├── wsgi.py                  # WSGI application entry point
└── asgi.py                  # ASGI application entry point
```

## Core Components

### 1. Settings (`settings.py`)

**Main Configuration File**

This file contains all the Django project settings and configurations:

#### **Core Django Settings**
- `SECRET_KEY`: Django secret key (loaded from environment)
- `DEBUG`: Debug mode configuration
- `ALLOWED_HOSTS`: Permitted host/domain names
- `INSTALLED_APPS`: List of installed Django applications
- `MIDDLEWARE`: Request/response processing middleware stack

#### **Database Configuration**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```
- PostgreSQL database configuration
- Environment variable-based credentials
- Secure credential management

#### **Django REST Framework Configuration**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```
- JWT authentication as default
- Authenticated access requirement
- REST API behavior configuration

#### **JWT Configuration**
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```
- Token lifetime management
- Security configurations
- Token rotation policies

#### **Security Settings**
- Password validation requirements
- CORS configuration (if needed)
- Security middleware configuration
- Environment-based sensitive data loading

#### **Internationalization**
- `LANGUAGE_CODE`: Default language setting
- `TIME_ZONE`: Application timezone
- `USE_I18N`: Internationalization support
- `USE_TZ`: Timezone support

#### **Static Files Configuration**
- `STATIC_URL`: Static files URL prefix
- `STATIC_ROOT`: Static files collection directory
- `STATICFILES_DIRS`: Additional static files directories

### 2. URL Configuration (`urls.py`)

**Root URL Routing**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

**URL Structure:**
- `admin/`: Django admin interface
- `api/`: All API endpoints (delegated to api.urls)

**Features:**
- Modular URL organization
- Clean API versioning structure
- Admin interface integration

### 3. WSGI Configuration (`wsgi.py`)

**Web Server Gateway Interface**

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_summary_project.settings')
application = get_wsgi_application()
```

**Purpose:**
- Production deployment interface
- WSGI server integration (Gunicorn, uWSGI)
- Environment configuration

### 4. ASGI Configuration (`asgi.py`)

**Asynchronous Server Gateway Interface**

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_summary_project.settings')
application = get_asgi_application()
```

**Purpose:**
- Asynchronous deployment support
- WebSocket support (future expansion)
- Modern async server compatibility

## Environment Variables

The project uses environment variables for sensitive configuration:

### Required Variables
```bash
# Django Configuration
SECRET_KEY='your-django-secret-key'

# Database Configuration
DB_NAME='news_summary_db'
DB_USER='your_postgres_user'
DB_PASSWORD='your_postgres_password'
DB_HOST='localhost'
DB_PORT='5432'

# External APIs
NEWS_API_KEY='your-newsapi-key'
```

### Loading Mechanism
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
```

## Security Features

### 1. Environment-Based Configuration
- No hardcoded secrets in source code
- `.env` file for local development
- Environment variables for production

### 2. Django Security Middleware
- CSRF protection
- XSS protection
- Content type sniffing protection
- Referrer policy enforcement

### 3. JWT Security
- Short-lived access tokens (5 minutes)
- Secure refresh token rotation
- Token blacklisting after rotation

### 4. Database Security
- Parameterized queries (Django ORM)
- Connection pooling
- Secure credential storage

## Deployment Configuration

### Development
```bash
python manage.py runserver
```

### Production (WSGI)
```bash
gunicorn news_summary_project.wsgi:application
```

### Production (ASGI)
```bash
uvicorn news_summary_project.asgi:application
```

## Application Registry

The project manages these Django applications:

### Core Django Apps
- `django.contrib.admin`: Admin interface
- `django.contrib.auth`: Authentication system
- `django.contrib.contenttypes`: Content type framework
- `django.contrib.sessions`: Session framework
- `django.contrib.messages`: Messaging framework
- `django.contrib.staticfiles`: Static file serving

### Third-Party Apps
- `rest_framework`: Django REST Framework
- `rest_framework_simplejwt`: JWT authentication

### Custom Apps
- `api`: Main API application

## Database Management

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Database Commands
```bash
python manage.py createsuperuser  # Create admin user
python manage.py dbshell          # Database shell
python manage.py shell            # Django shell
```

## Monitoring and Logging

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Performance Optimization

### Database Optimization
- Connection pooling
- Query optimization
- Index management

### Caching Strategy
- Redis integration (future)
- Database query caching
- Static file caching

## Testing Configuration

### Test Database
- Separate test database
- Faster test execution
- Isolated test environment

### Test Settings
```python
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
```

## Maintenance Commands

### Regular Maintenance
```bash
python manage.py collectstatic    # Collect static files
python manage.py check            # System check
python manage.py migrate          # Apply migrations
```

### Custom Commands
```bash
python manage.py clear_articles   # Clear saved articles
```

This module serves as the foundation for the entire News Summary API, providing robust configuration, security, and deployment capabilities.
