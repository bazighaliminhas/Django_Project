from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    contact_no = models.CharField(max_length=20, default="")  # default for migrations

    def __str__(self):
        return self.username


class TempUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    contact_no = models.CharField(max_length=20)
    token = models.CharField(max_length=50, unique=True)



class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)  # UUID for security
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.token}"
