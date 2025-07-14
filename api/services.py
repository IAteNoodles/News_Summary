import os
import requests
from dotenv import load_dotenv
from transformers import pipeline
import logging

load_dotenv()

# Get a logger instance
logger = logging.getLogger(__name__)

# Global variable to hold the summarization pipeline
# This uses lazy loading: the model is only loaded into memory when first needed.
summarizer_pipeline = None

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
    Summarizes the given text using a lightweight DistilBART model for speed.
    """
    global summarizer_pipeline

    # --- Robustness Check ---
    # If the input text is empty, None, or just whitespace, return immediately.
    if not text or not text.strip():
        return "Content was empty or could not be scraped. No summary available."
    # --- End Check ---

    # --- Model Change ---
    # We are changing the model, so we must reset the pipeline to force re-initialization.
    if summarizer_pipeline and summarizer_pipeline.model.name_or_path != "sshleifer/distilbart-cnn-12-6":
        logger.info("Model change detected. Resetting pipeline.")
        summarizer_pipeline = None
    # --- End Model Change ---

    # Lazy-load the pipeline to avoid loading the model on server startup
    if summarizer_pipeline is None:
        logger.info("Initializing lightweight summarization pipeline (distilbart)...")
        # This model is much smaller and faster.
        summarizer_pipeline = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
        )
        logger.info("Pipeline initialized.")

    try:
        # --- Automatic Truncation ---
        # We let the pipeline handle truncation. It knows the model's exact
        # token limit and will truncate the text correctly.
        summary_list = summarizer_pipeline(text, truncation=True)
        # --- End Automatic Truncation ---
        
        return summary_list[0]['summary_text']
    except IndexError:
        # This can happen if the model returns an empty list, e.g., for very short text
        logger.warning(f"Summarizer returned an empty list for text: '{text[:100]}...'")
        return "Summary could not be generated for the provided text."
    except Exception as e:
        # Log the full exception traceback for better debugging
        logger.exception(f"Error during summarization: {e}")
        return "Error during summarization. Could not process content."