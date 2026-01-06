from rest_framework import serializers
from .models import Book, Author
from categories.models import Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    # Display names in API responses
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    
    # Accept IDs in POST/PUT/PATCH requests
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'category', 'category_name', 'price']


    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
