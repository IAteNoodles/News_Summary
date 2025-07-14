# News Summary API

This project is a secure and efficient backend API for a News Summary Application, built with Django and Django REST Framework. It fetches news from the NewsAPI, summarizes the content using a local AI model from the Hugging Face Transformers library, and allows users to save and retrieve their favorite articles.

## Core Technologies

- **Backend:** Django & Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** JSON Web Tokens (JWT)
- **AI Summarization:** Hugging Face Transformers (`sshleifer/distilbart-cnn-12-6`)
- **External APIs:** [NewsAPI](https://newsapi.org/)

## Features

- Secure user registration and login endpoints using JWT.
- Fetch latest news headlines.
- Search for news articles based on a query.
- AI-powered summarization of news content previews.
- Authenticated endpoints to save articles to a user's account.
- Endpoint to view all saved articles for the logged-in user.

---

## Project Setup

Follow these steps to get the project running locally.

### 1. Prerequisites

- Python 3.11
- PostgreSQL installed and a database created.
- `git` for cloning the repository.

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd DjangoIntern
```

### 3. Set up the Python Environment

It is highly recommended to use a virtual environment.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Or on Windows
# .venv\Scripts\activate
```

### 4. Install Dependencies

Install all required packages using the provided `pyproject.toml` with `uv` (or `pip`).

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt 
# Note: You will need to create a requirements.txt file first if it doesn't exist:
# pip freeze > requirements.txt
```

### 5. Environment Variables

This project requires a `.env` file in the root directory to store sensitive information.

**Create a file named `.env`** in the project root and add the following variables.

```env
# Django Secret Key (generate a new one for production)
SECRET_KEY='django-insecure-_7(@9qxnp*92np+c&e_+p!v*b%&awn$!^9@9ril^!)%1(+w57+'

# NewsAPI Key (get your free key from https://newsapi.org/)
NEWS_API_KEY='YOUR_NEWS_API_KEY_HERE'

# PostgreSQL Database Credentials
DB_NAME='news_summary_db'
DB_USER='your_db_user'
DB_PASSWORD='your_db_password'
DB_HOST='localhost'
DB_PORT='5432'
```
**Important:** You must update the `DATABASES` setting in `news_summary_project/settings.py` to use these environment variables.

### 6. Database Migrations

Apply the database schema to your PostgreSQL database.

```bash
python manage.py migrate
```

### 7. Run the Server

Start the Django development server. The AI model will be downloaded and loaded into memory on the first startup, which may take a few moments.

```bash
python manage.py runserver
```

The API will now be running at `http://127.0.0.1:8000/`.

---

## API Endpoints Guide

All protected endpoints require an `Authorization: Bearer <YOUR_ACCESS_TOKEN>` header.

### Authentication

#### 1. Register a New User

- **Endpoint:** `POST /api/register/`
- **Description:** Creates a new user account.
- **Body:**
  ```json
  {
      "username": "newuser",
      "email": "user@example.com",
      "password": "a-strong-password"
  }
  ```
- **Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "user@example.com", "password": "a-strong-password"}' \
  http://127.0.0.1:8000/api/register/
  ```

#### 2. Obtain JWT (Login)

- **Endpoint:** `POST /api/token/`
- **Description:** Authenticates a user and returns an `access` and `refresh` token pair.
- **Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "a-strong-password"}' \
  http://127.0.0.1:8000/api/token/
  ```

### News

#### 3. Get Latest News

- **Endpoint:** `GET /api/latest/`
- **Description:** Fetches and summarizes the latest news headlines.
- **Example:**
  ```bash
  curl -X GET -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" http://127.0.0.1:8000/api/latest/
  ```

#### 4. Search News

- **Endpoint:** `GET /api/search/?q=<query>`
- **Description:** Searches for and summarizes news based on a search term.
- **Example:**
  ```bash
  curl -X GET -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" "http://127.0.0.1:8000/api/search/?q=Tesla"
  ```

### Saved Articles

#### 5. Save an Article

- **Endpoint:** `POST /api/save/`
- **Description:** Saves a news article to the logged-in user's account.
- **Body:**
  ```json
  {
      "title": "Example Article Title",
      "url": "https://example.com/article",
      "source_name": "Example News",
      "summary": "This is the AI-generated summary of the article.",
      "published_at": "2025-07-14T12:00:00Z"
  }
  ```
- **Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -d '{"title": "...", "url": "...", "source_name": "...", "summary": "...", "published_at": "..."}' \
  http://127.0.0.1:8000/api/save/
  ```

#### 6. View Saved Articles

- **Endpoint:** `GET /api/saved/`
- **Description:** Retrieves a list of all articles saved by the logged-in user.
- **Example:**
  ```bash
  curl -X GET -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" http://127.0.0.1:8000/api/saved/
  ```
