# api/urls.py
from django.urls import path
# Make sure to import the new views
from .views import (
    UserRegistrationView, 
    LatestNewsView, 
    SearchNewsView, 
    SaveNewsView, 
    SavedNewsView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Keep the existing auth paths
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Add the new paths for the news API
    path('latest/', LatestNewsView.as_view(), name='latest-news'),
    path('search/', SearchNewsView.as_view(), name='search-news'),
    path('save/', SaveNewsView.as_view(), name='save-news'),
    path('saved/', SavedNewsView.as_view(), name='saved-news'),
]

