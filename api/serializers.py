# api/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Article

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.
    """
    class Meta:
        model = Article
        # We exclude the 'user' field because it will be set automatically
        # in the view based on the logged-in user.why
        fields = ('id', 'title', 'url', 'source_name', 'summary', 'published_at', 'saved_at')
        read_only_fields = ('saved_at',)