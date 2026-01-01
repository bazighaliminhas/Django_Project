from rest_framework import serializers
from .models import Book, Author
from categories.models import Category
from categories.serializers import CategorySerializer

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)  # 👈 NEW

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'category', 'category_name', 'price']
