from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                firstname = user.full_name.split()[0]
                login(request, user)
                token = get_tokens_for_user(user)
                return Response({
                    "FirstName": firstname,
                    "UserId": user.id,
                    "Token": token['access'],
                    "UserType": user.role
                }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get("Email")
        password = request.data.get("Password")
        user = authenticate(request, email=email, password=password)
        if user:
            firstname = user.full_name.split()[0]
            login(request, user)
            token = get_tokens_for_user(user)
            return Response({
                "FirstName": firstname,
                "UserId": user.id,
                "Token": token['access'],
                "UserType": user.role
            }, status=status.HTTP_200_OK)
        
        return Response({
            "message": "Email atau password salah!"
        }, status=status.HTTP_400_BAD_REQUEST)

