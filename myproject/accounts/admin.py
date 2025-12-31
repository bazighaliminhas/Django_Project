from django.contrib import admin
from .models import User, TempUser

# Register models individually
admin.site.register(User)
admin.site.register(TempUser)