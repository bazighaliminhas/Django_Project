from django.urls import path
from .views import (
    register, verify_email, login,
    get_all_users, delete_user, update_user,
    forgot_password, reset_password
)

urlpatterns = [
    path('register/', register),
    path('verify/<str:token>/', verify_email),
    path('login/', login),

    path('forgot-password/', forgot_password),
    path('reset-password/<str:token>/', reset_password),

    path('users/', get_all_users),
    path('users/delete/<int:user_id>/', delete_user),
    path('users/update/<int:user_id>/', update_user),
]
