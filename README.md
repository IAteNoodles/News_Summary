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
    cd DjangoIntern
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
