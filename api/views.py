from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import services
from .models import Article
from .serializers import ArticleSerializer
from django.db.models import QuerySet
from .scraper import scrape_article_text # Import the scraper
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    An endpoint for registering a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class LatestNewsView(APIView):
    """
    Fetches the latest news, summarizes them, and returns them.
    This endpoint does not interact with the database.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news_data = services.fetch_from_news_api()
        if 'error' in news_data:
            return Response(news_data, status=500)

        articles = []
        for article_data in news_data.get('articles', []):
            # Ensure article_data is a dictionary before processing
            if not isinstance(article_data, dict):
                continue
            
            # --- Scraper Integration ---
            text_to_summarize = None
            scraped_content = scrape_article_text(article_data.get('url'))
            
            if scraped_content:
                text_to_summarize = scraped_content
            else:
                text_to_summarize = article_data.get('content') or article_data.get('description')

            # --- End Scraper Integration ---

            # --- New Summarization Logic ---
            summary = ""
            original_description = article_data.get('description') or ""

            if text_to_summarize and text_to_summarize.strip():
                # Only run the summarizer if we have actual text
                summary = services.summarize_text(text_to_summarize)
                logger.info(f"SUCCESS (Summarizer): Summarized {article_data.get('url')}")
            else:
                logger.warning(f"No content found for summarization for {article_data.get('url')}.")

            # Final fallback: if summary is still empty, use the original description.
            if not summary.strip():
                summary = original_description or "No summary available."
                logger.info(f"FALLBACK (Final): Using API description for {article_data.get('url')}")
            # --- End New Summarization Logic ---

            articles.append({
                'title': article_data.get('title'),
                'url': article_data.get('url'),
                'source_name': article_data.get('source', {}).get('name'),
                'summary': summary,
                'published_at': article_data.get('publishedAt'),
            })
        return Response(articles)


class SearchNewsView(APIView):
    """
    Searches for news based on a query parameter, summarizes, and returns them.
    This endpoint does not interact with the database.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', None)
        if not query:
            return Response({'error': 'Query parameter "q" is required.'}, status=400)

        news_data = services.fetch_from_news_api(search_term=query)
        if 'error' in news_data:
            return Response(news_data, status=500)

        articles = []
        for article_data in news_data.get('articles', []):
            # Ensure article_data is a dictionary before processing
            if not isinstance(article_data, dict):
                continue

            # --- Scraper Integration ---
            text_to_summarize = None
            scraped_content = scrape_article_text(article_data.get('url'))

            if scraped_content:
                text_to_summarize = scraped_content
            else:
                text_to_summarize = article_data.get('content') or article_data.get('description')
            # --- End Scraper Integration ---

            # --- New Summarization Logic ---
            summary = ""
            original_description = article_data.get('description') or ""

            if text_to_summarize and text_to_summarize.strip():
                # Only run the summarizer if we have actual text
                summary = services.summarize_text(text_to_summarize)
                logger.info(f"SUCCESS (Summarizer): Summarized {article_data.get('url')}")
            else:
                logger.warning(f"No content found for summarization for {article_data.get('url')}.")

            # Final fallback: if summary is still empty, use the original description.
            if not summary.strip():
                summary = original_description or "No summary available."
                logger.info(f"FALLBACK (Final): Using API description for {article_data.get('url')}")
            # --- End New Summarization Logic ---

            articles.append({
                'title': article_data.get('title'),
                'url': article_data.get('url'),
                'source_name': article_data.get('source', {}).get('name'),
                'summary': summary,
                'published_at': article_data.get('publishedAt'),
            })
        return Response(articles)


class SaveNewsView(generics.CreateAPIView):
    """
    Saves a news article to the logged-in user's account.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the article with the logged-in user.
        serializer.save(user=self.request.user)


class SavedNewsView(generics.ListAPIView):
    """
    Lists all news articles saved by the logged-in user.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Article]:
        """
        Filter articles to only show those belonging to the current user.
        """
        return Article.objects.filter(user=self.request.user).order_by('-saved_at')
