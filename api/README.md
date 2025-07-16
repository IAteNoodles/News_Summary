# API Module

This module contains the core API functionality for the News Summary application. It handles user authentication, news fetching, article scraping, AI summarization, and article management.

## Module Structure

```
api/
├── __init__.py              # Package initialization
├── admin.py                 # Django admin interface configuration
├── apps.py                  # App configuration
├── models.py                # Database models
├── serializers.py           # DRF serializers for data validation
├── services.py              # External service integrations
├── scraper.py               # Web scraping functionality
├── views.py                 # API endpoints and business logic
├── urls.py                  # URL routing for API endpoints
├── tests.py                 # Unit tests
├── management/              # Django management commands
│   └── commands/
│       └── clear_articles.py
└── migrations/              # Database migrations
```

## Core Components

### 1. Models (`models.py`)

**Article Model**
- Represents a saved news article in the database
- Fields:
  - `user`: Foreign key to Django's User model
  - `title`: Article title (CharField, max 255 chars)
  - `url`: Article URL (URLField, unique)
  - `source_name`: News source name (CharField, max 100 chars)
  - `summary`: AI-generated summary (TextField)
  - `published_at`: Article publication date (DateTimeField)
  - `saved_at`: When the article was saved (auto-populated)
- Constraints:
  - `unique_together`: Prevents duplicate articles per user

### 2. Serializers (`serializers.py`)

**UserRegistrationSerializer**
- Handles user registration validation
- Fields: username, password, email
- Custom `create()` method for secure user creation

**ArticleSerializer**
- Handles article data validation and serialization
- Used for both saving and retrieving articles
- Automatically handles JSON serialization/deserialization

### 3. Services (`services.py`)

**External Service Integration Layer**

**`fetch_from_news_api(search_term=None)`**
- Integrates with NewsAPI.org
- Fetches latest news or searches by keyword
- Returns structured news data
- Handles API errors gracefully

**`initialize_summarizer()`**
- Initializes the AI summarization pipeline
- Uses HuggingFace transformers library
- Model: `sshleifer/distilbart-cnn-12-6`
- Optimized for news summarization

**`summarize_text(text)`**
- Generates AI-powered summaries
- Handles text length limitations
- Returns concise summaries for news articles

### 4. Web Scraper (`scraper.py`)

**Article Content Extraction**

**`scrape_article_text(url)`**
- Extracts full article content from news URLs
- Multi-heuristic approach:
  1. **Semantic Element Search**: Looks for `<article>`, `<main>`, etc.
  2. **CSS Selector Fallback**: Uses common content selectors
  3. **Paragraph Density Analysis**: Finds content-rich sections
- Handles various news site structures
- Returns clean, readable text

**Features:**
- Robust error handling
- User-agent rotation
- Content cleaning and normalization
- Fallback strategies for different site layouts

### 5. Views (`views.py`)

**API Endpoints Implementation**

**Authentication Views:**
- `UserRegistrationView`: User registration endpoint
- JWT token endpoints (provided by `djangorestframework-simplejwt`)

**News Views:**
- `LatestNewsView`: Fetches and summarizes latest news
- `SearchNewsView`: Searches and summarizes news by query
- `SaveNewsView`: Saves articles to user's account
- `SavedNewsView`: Retrieves user's saved articles

**Features:**
- JWT authentication required for all news endpoints
- Integrated scraping and summarization pipeline
- Graceful error handling with fallbacks
- Automatic user association for saved articles

### 6. URL Configuration (`urls.py`)

**API Routing**
- `/register/`: User registration
- `/token/`: Login (get access/refresh tokens)
- `/token/refresh/`: Refresh access token
- `/latest/`: Get latest news with summaries
- `/search/?q=<query>`: Search news with summaries
- `/save/`: Save an article
- `/saved/`: Get saved articles

### 7. Management Commands (`management/commands/`)

**`clear_articles.py`**
- Custom Django management command
- Usage: `python manage.py clear_articles`
- Clears all saved articles from the database
- Useful for testing and development

## Key Features

### 1. AI-Powered Summarization
- Uses state-of-the-art transformer models
- Automatically generates concise summaries
- Fallback to original descriptions when needed

### 2. Intelligent Web Scraping
- Multi-strategy content extraction
- Handles modern JavaScript-heavy sites
- Robust error handling and recovery

### 3. Secure Authentication
- JWT-based authentication
- Token refresh mechanism
- User isolation for saved articles

### 4. Scalable Architecture
- Service layer separation
- Modular design
- Easy to extend and maintain

## Database Integration

The API uses PostgreSQL through Django's ORM:
- **User Management**: Built-in Django User model
- **Article Storage**: Custom Article model with user relationships
- **Migrations**: Automatic schema management

## Error Handling

The API implements comprehensive error handling:
- External API failures
- Web scraping errors
- AI model failures
- Database connection issues

Each component includes fallback mechanisms to ensure system reliability.

## Testing

Run the API tests with:
```bash
python manage.py test api
```

## Usage Examples

### Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'
```

### Get Latest News
```bash
curl -X GET http://127.0.0.1:8000/api/latest/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Save an Article
```bash
curl -X POST http://127.0.0.1:8000/api/save/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "News Title", "url": "https://example.com/article", "source_name": "Example News", "summary": "Article summary", "published_at": "2025-07-16T10:00:00Z"}'
```
