from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Category
from .serializers import CategorySerializer
from accounts.permissions import IsEmailAdmin

# ---------------- Swagger Request Body for Category ----------------
category_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['name'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Category description', default='')
    }
)

# ---------------- List Categories (USER + ADMIN) ----------------
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Filter by category name", type=openapi.TYPE_STRING)
    ],
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_categories(request):
    name = request.GET.get('name')
    categories = Category.objects.all()

    if name:
        categories = categories.filter(name__icontains=name)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# ---------------- Category CRUD (ADMIN ONLY) ----------------
@swagger_auto_schema(method='post', request_body=category_request_body, responses={201: CategorySerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(methods=['put', 'patch'], request_body=category_request_body)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"message": "Category not found"}, status=404)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsEmailAdmin])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response(status=204)  # RESTful DELETE
    except Category.DoesNotExist:
        return Response({"message": "Category not found"}, status=404)
