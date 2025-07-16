# News Summary API

This project is a Django-based REST API that fetches news from an external source, summarizes it using an AI model, and allows users to save their favorite articles.

## Core Technologies

*   **Backend**: Django, Django REST Framework
*   **Database**: PostgreSQL (via `psycopg2-binary`)
*   **Authentication**: JSON Web Tokens (`djangorestframework-simplejwt`)
*   **AI Summarization**: `transformers` library
*   **Web Scraping**: `requests` and `BeautifulSoup`

## Requirements

*   **Python**: 3.11+
*   **PostgreSQL**: A running instance of PostgreSQL.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/IAteNoodles/News_Summary.git
    cd News_Summary
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root directory. This file will hold your sensitive information. Add the following variables, adjusting the database values for your local PostgreSQL setup:

    ```
    SECRET_KEY='your-django-secret-key'
    NEWS_API_KEY='your-newsapi-key'
    
    DB_NAME='news_summary_db'
    DB_USER='your_postgres_user'
    DB_PASSWORD='your_postgres_password'
    DB_HOST='localhost'
    DB_PORT='5432'
    ```
    *   You can generate a new Django `SECRET_KEY` using an online generator.
    *   Get your `NEWS_API_KEY` from [newsapi.org](https://newsapi.org/).

5.  **Run initial database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

All endpoints require JWT authentication. You must include an `Authorization: Bearer <your_access_token>` header in your requests.

### Authentication

*   **`POST /api/register/`**
    *   Register a new user.
    *   **Body**: `{ "username": "youruser", "password": "yourpassword", "email": "user@example.com" }`

*   **`POST /api/token/`**
    *   Log in to get an access and refresh token pair.
    *   **Body**: `{ "username": "youruser", "password": "yourpassword" }`

*   **`POST /api/token/refresh/`**
    *   Get a new access token using a refresh token.
    *   **Body**: `{ "refresh": "your_refresh_token" }`

**Note on Token Lifetimes:** By default, `djangorestframework-simplejwt` has the following token lifetimes:
*   **Access Token**: 5 minutes
*   **Refresh Token**: 24 hours

These can be configured in `settings.py` if needed.

### News

*   **`GET /api/latest/`**
    *   Fetches the latest news articles, scrapes them for full content, generates new summaries, and returns the results.

*   **`GET /api/search/?q=<query>`**
    *   Searches for news articles matching the `<query>`, scrapes them, generates summaries, and returns the results.

### Saved Articles

*   **`POST /api/save/`**
    *   Saves a news article to your account.
    *   **Body**: `{ "title": "...", "url": "...", "source_name": "...", "summary": "...", "published_at": "..." }`

*   **`GET /api/saved/`**
    *   Retrieves a list of all articles you have saved.

## Project Structure

This project is organized into several modules, each with its own specific purpose:

```
DjangoIntern/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── news_summary_project/       # Django project configuration
│   ├── README.md               # Project module documentation
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── api/                        # Main API application
│   ├── README.md               # API module documentation
│   ├── models.py               # Database models
│   ├── views.py                # API endpoints
│   ├── serializers.py          # Data serializers
│   ├── services.py             # External service integration
│   ├── scraper.py              # Web scraping functionality
│   ├── urls.py                 # API URL routing
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── tests.py                # Unit tests
│   ├── management/             # Custom management commands
│   │   ├── README.md           # Management commands documentation
│   │   └── commands/
│   │       └── clear_articles.py
│   └── migrations/             # Database migrations
├── test_files/                 # Development testing scripts
│   ├── api_test_client.py      # API testing client
│   ├── test_news_api.py        # NewsAPI testing
│   └── test_single_scraper.py  # Scraper testing
└── scripts/                    # Deployment and setup scripts
    ├── setup_and_test.sh       # Setup automation
    └── full_clone_test.sh      # Complete testing script
```

## Module Documentation

Each module has its own detailed README file:

- **[`news_summary_project/README.md`](news_summary_project/README.md)**: Django project configuration, settings, security, and deployment
- **[`api/README.md`](api/README.md)**: API endpoints, models, services, scraping, and authentication
- **[`api/management/README.md`](api/management/README.md)**: Custom Django management commands

## Key Features

### 🔐 Secure Authentication
- JWT-based authentication with refresh tokens
- User registration and login endpoints
- Token expiration and refresh mechanisms

### 🤖 AI-Powered Summarization
- Uses HuggingFace transformers for article summarization
- Model: `sshleifer/distilbart-cnn-12-6`
- Intelligent fallback to original descriptions

### 🕷️ Intelligent Web Scraping
- Multi-strategy content extraction
- Handles modern JavaScript-heavy websites
- Robust error handling and recovery

### 📊 PostgreSQL Integration
- Secure database configuration
- User-specific article storage
- Efficient query optimization

### 🔧 Management Tools
- Custom Django management commands
- Database maintenance utilities
- Development and testing helpers

## Architecture Overview

### Service Layer Architecture
```
Client Request → Authentication → Views → Services → External APIs
                                     ↓
                                Scraping → AI Summarization
                                     ↓
                                Database Storage
```

### Data Flow
1. **Authentication**: JWT token validation
2. **News Fetching**: NewsAPI integration
3. **Content Scraping**: Full article extraction
4. **AI Summarization**: Transformer-based summarization
5. **Data Storage**: PostgreSQL with user relationships

## Development Workflow

### Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/IAteNoodles/News_Summary.git
cd News_Summary
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing
```bash
# Run all tests
python manage.py test

# Test specific module
python manage.py test api

# Test with coverage
coverage run --source='.' manage.py test
coverage report
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Clear articles (custom command)
python manage.py clear_articles
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper database credentials
- [ ] Set up environment variables
- [ ] Configure static file serving
- [ ] Set up proper logging
- [ ] Configure CORS if needed
- [ ] Set up monitoring and alerts

### Docker Deployment (Future)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "news_summary_project.wsgi:application"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is developed as part of an internship assignment.

## Support

For technical questions or issues:
1. Check the module-specific README files
2. Review the Django documentation
3. Check the API endpoint documentation
4. Review the test files for usage examples
