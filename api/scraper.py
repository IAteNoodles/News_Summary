import requests
from bs4 import BeautifulSoup, NavigableString
import logging

# Get a logger instance for this module
logger = logging.getLogger(__name__)

def scrape_article_text(url):
    """
    Scrapes the main article text from a given URL using requests and BeautifulSoup.
    This version does not render JavaScript but is more stable and uses multiple heuristics.

    Args:
        url (str): The URL of the news article to scrape.

    Returns:
        str: The extracted article text, or None if scraping fails.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'lxml')

        # --- Heuristic 1: Try a list of common, specific selectors first ---
        selectors = [
            'article',
            'main',
            'div[role="article"]',
            'div.article-body',
            'div.story-content',
            'div#main-content',
            'div#content',
            'div.post-content',
            'div.entry-content',
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                if len(text) > 250:  # Increased threshold for better quality
                    logger.info(f"Successfully scraped content from {url} using selector: '{selector}'.")
                    return text

        # --- Heuristic 2: Paragraph-based density search (advanced fallback) ---
        # If specific containers fail, find the parent element with the most paragraph text.
        all_paragraphs = soup.find_all('p')
        if not all_paragraphs:
            logger.warning(f"No <p> tags found on {url}. Cannot use density search.")
            return None

        top_parent = None
        max_text_len = 0

        for p in all_paragraphs:
            parent = p.parent
            if parent:
                text_len = len(parent.get_text(separator=' ', strip=True))
                if text_len > max_text_len:
                    max_text_len = text_len
                    top_parent = parent
        
        if top_parent:
            # Clean up the extracted text by removing common noise (nav, footer, etc.)
            for tag in top_parent.find_all(['nav', 'footer', 'aside', 'header', 'script', 'style']):
                tag.decompose()
            
            text = top_parent.get_text(separator=' ', strip=True)
            if len(text) > 250:
                logger.info(f"Successfully scraped content from {url} using paragraph density search.")
                return text

        logger.warning(f"Could not find sufficient content on {url} using any heuristic.")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
        return None
