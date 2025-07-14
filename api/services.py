import os
import requests
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

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

    # Lazy-load the pipeline to avoid loading the model on server startup
    if summarizer_pipeline is None:
        print("Initializing lightweight summarization pipeline (distilbart)...")
        # This model is much smaller and faster than Phi-4
        summarizer_pipeline = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
        )
        print("Pipeline initialized.")

    if not text or not isinstance(text, str):
        return "No text provided for summarization."

    try:
        print("Generating summary with distilbart...")
        # The summarization pipeline is simpler and takes the text directly.
        # It also has its own parameters for controlling length.
        results = summarizer_pipeline(text, max_length=150, min_length=30, do_sample=False)
        summary = results[0]['summary_text']
        print("Summary generated successfully.")
        return summary.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        # Fallback to simple truncation if the model fails
        return text[:150] + "..."