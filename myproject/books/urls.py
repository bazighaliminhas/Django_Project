from django.urls import path
from .views import ( 
    list_books, add_book, update_book, delete_book, list_authors, 
    add_author, update_author, delete_author ) 
urlpatterns = [ # Book URLs 
               path('books/', list_books), 
               path('books/add/', add_book), 
               path('books/update/<int:book_id>/', update_book), 
               path('books/delete/<int:book_id>/', delete_book), 
               # Author URLs 
               path('authors/', list_authors), 
               path('authors/add/', add_author), 
               path('authors/update/<int:author_id>/', update_author), 
               path('authors/delete/<int:author_id>/', delete_author), 
               ] 