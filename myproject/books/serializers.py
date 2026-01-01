from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.SerializerMethodField()  # Optional: show category name

    class Meta:
        model = Book
        fields = ['id', 'title',  'author_name', 'category_name', 'price']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
