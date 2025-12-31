from django.db import models 
# Create your models here. 
class Author(models.Model): 
    name = models.CharField(max_length=100) 
    bio = models.TextField(blank=True, null=True) 
    def __str__(self): 
        return self.name 
    
    
class Book(models.Model): 
    title = models.CharField(max_length=200) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    def __str__(self): 
        return self.title 
    
    