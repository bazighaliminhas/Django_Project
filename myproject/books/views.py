from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from accounts.permissions import IsEmailAdmin


# ---------------- Swagger Request Body for Book ----------------
book_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['title', 'author', 'price'],
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Book title'),
        'author': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
        'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Book price')
    }
)

# ---------------- Swagger Request Body for Author ----------------
author_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['name'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Author name'),
        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Author bio', default='')
    }
)

# ---------------- List Books (USER + ADMIN) ----------------
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Search by book title", type=openapi.TYPE_STRING),
        openapi.Parameter('author', openapi.IN_QUERY, description="Search by author name", type=openapi.TYPE_STRING)
    ],
    responses={200: BookSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_books(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    books = Book.objects.all()

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__name__icontains=author)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# ---------------- Book CRUD (ADMIN ONLY) ----------------
@swagger_auto_schema(method='post', request_body=book_request_body, responses={201: BookSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=book_request_body)
@swagger_auto_schema(method='patch', request_body=book_request_body)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def update_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"message": "Book not found"}, status=404)

    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response({"message": "Book deleted successfully"})
    except Book.DoesNotExist:
        return Response({"message": "Book not found"}, status=404)


# ---------------- List Authors (USER + ADMIN) ----------------
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Search by author name", type=openapi.TYPE_STRING)
    ],
    responses={200: AuthorSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_authors(request):
    name = request.GET.get('name')

    # Admin sees all authors
    if hasattr(request.user, 'email') and request.user.email == "bazighaliminhas1@gmail.com":
        authors = Author.objects.all()
    else:
        # Regular users can filter by name
        authors = Author.objects.all()
        if name:
            authors = authors.filter(name__icontains=name)

    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


# ---------------- Author CRUD (ADMIN ONLY) ----------------
@swagger_auto_schema(method='post', request_body=author_request_body, responses={201: AuthorSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def add_author(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='put', request_body=author_request_body)
@swagger_auto_schema(method='patch', request_body=author_request_body)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def update_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({"message": "Author not found"}, status=404)

    serializer = AuthorSerializer(author, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def delete_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        author.delete()
        return Response({"message": "Author deleted successfully"})
    except Author.DoesNotExist:
        return Response({"message": "Author not found"}, status=404)



