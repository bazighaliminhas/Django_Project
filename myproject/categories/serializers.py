from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'books']

    def get_books(self, obj):
        # Lazy import here to avoid circular import
        from books.serializers import BookSerializer
        from books.models import Book

        books = Book.objects.filter(category=obj)
        return BookSerializer(books, many=True).data
