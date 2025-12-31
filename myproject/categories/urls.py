from django.urls import path
from .views import list_categories, add_category, update_category, delete_category

urlpatterns = [
    path('categories/', list_categories, name='list-categories'),              # GET list
    path('categories/add/', add_category, name='add-category'),                # POST add
    path('categories/update/<int:category_id>/', update_category, name='update-category'),  # PUT / PATCH
    path('categories/delete/<int:category_id>/', delete_category, name='delete-category'),  # DELETE
]
