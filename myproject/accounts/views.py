from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import User, TempUser, AuthToken
from .serializer import UserSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import User, PasswordResetToken

# Forgot Password
forgot_password_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

# Reset Password
reset_password_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['new_password'],
    properties={
        'new_password': openapi.Schema(type=openapi.TYPE_STRING),
    }
)




# Swagger Schemas
register_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'email', 'password', 'contact_no'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_no': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

# ---------------- Register ----------------
@swagger_auto_schema(method='post', request_body=register_request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    if User.objects.filter(email=data['email']).exists():
        return Response({"message": "Email already registered"}, status=400)

    TempUser.objects.filter(email=data['email']).delete()
    token = get_random_string(32)

    TempUser.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password']),
        contact_no=data['contact_no'],
        token=token
    )

    verify_link = f"http://127.0.0.1:8000/api/verify/{token}/"
    send_mail(
        'Verify your email',
        f'Click the link to verify: {verify_link}',
        settings.EMAIL_HOST_USER,
        [data['email']],
    )

    return Response({"message": "Verification email sent"})


# ---------------- Verify Email ----------------
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        temp_user = TempUser.objects.get(token=token)
        user = User.objects.create(
            username=temp_user.username,
            email=temp_user.email,
            password=temp_user.password,
            contact_no=temp_user.contact_no
        )
        temp_user.delete()

        # Create token automatically
        token_obj = AuthToken.objects.create(user=user)

        return Response({
            "message": "Email verified successfully",
            "token": str(token_obj.token)
        })
    except TempUser.DoesNotExist:
        return Response({"message": "Invalid or expired token"}, status=400)


# ---------------- Login ----------------
@swagger_auto_schema(method='post', request_body=login_request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    try:
        user = User.objects.get(email=data['email'])
        if not check_password(data['password'], user.password):
            return Response({"message": "Invalid password"}, status=400)

        token_obj, _ = AuthToken.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": str(token_obj.token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "contact_no": user.contact_no
            }
        })
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)


# ---------------- Logout ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    AuthToken.objects.filter(user=request.user).delete()
    return Response({"message": "Logged out successfully"})


# ---------------- Get Users ----------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data)


# ---------------- Delete User ----------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted"})
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)


# ---------------- Update User Swagger ----------------
update_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'contact_no': openapi.Schema(type=openapi.TYPE_STRING),
    }
)
# ---------------- Update User ----------------
@swagger_auto_schema(method='put', request_body=update_request_body)
@swagger_auto_schema(method='patch', request_body=update_request_body)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    partial = request.method == 'PATCH'

    serializer = UserUpdateSerializer(
        user,
        data=request.data,
        partial=partial
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User updated successfully",
            "user": serializer.data
        })

    return Response(serializer.errors, status=400)




# ---------------- Forgot Password ----------------

# Swagger schema
forgot_password_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Registered email of the user'),
    }
)

reset_password_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['new_password'],
    properties={
        'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password to reset'),
    }
)

# ---------------- Forgot Password API ----------------
@swagger_auto_schema(method='post', request_body=forgot_password_request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({"message": "Email is required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User with this email does not exist"}, status=404)

    # Remove any old tokens
    PasswordResetToken.objects.filter(user=user).delete()

    # Create a new reset token
    token = get_random_string(50)
    PasswordResetToken.objects.create(user=user, token=token)

    # Construct reset link
    reset_link = f"http://127.0.0.1:8000/api/reset-password/{token}/"

    # Send reset email
    send_mail(
        subject='Reset Your Password',
        message=f'Hello {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({"message": "Password reset email sent successfully"})


# ---------------- Reset Password API ----------------
@swagger_auto_schema(method='post', request_body=reset_password_request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
    try:
        reset_obj = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({"message": "Invalid or expired token"}, status=400)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({"message": "New password is required"}, status=400)

    user = reset_obj.user
    user.password = make_password(new_password)
    user.save()

    # Delete token after successful reset
    reset_obj.delete()

    return Response({"message": "Password reset successfully"})
