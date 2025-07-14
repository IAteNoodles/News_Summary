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
            original_content = article_data.get('content') or ""
            summary = services.summarize_text(original_content)
            articles.append({
                'title': article_data.get('title'),
                'url': article_data.get('url'),
                'source_name': article_data.get('source', {}).get('name'),
                'original_content': original_content,
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
            original_content = article_data.get('content') or ""
            summary = services.summarize_text(original_content)
            articles.append({
                'title': article_data.get('title'),
                'url': article_data.get('url'),
                'source_name': article_data.get('source', {}).get('name'),
                'original_content': original_content,
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
