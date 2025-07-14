import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_from_news_api(search_term=None):
    """
    Fetches news from the NewsAPI.
    Can fetch latest headlines or search for a specific term.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        # In a real application, you'd want more robust error handling
        # or logging here.
        return {"error": "NEWS_API_KEY environment variable not set."}

    if search_term:
        url = f"https://newsapi.org/v2/everything?q={search_term}&apiKey={api_key}"
    else:
        # Fetching top headlines from the US as a default
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        return {"error": f"API request failed: {e}"}

def summarize_text(text):
    """
    Placeholder for a text summarization function.
    In a real implementation, this would call an AI summarization service.
    For this project, we'll just return the first 150 characters.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # A simple truncation as a stand-in for a real summary
    summary = text[:150]
    if len(text) > 150:
        summary += "..."
    return summary