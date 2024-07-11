from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class SignupView(APIView):

    def post(self, request):
        data = request.data
        role = data.get('SignUpType', None)

        if not role:
            return Response({
                "Message": "SignUp harus menyertakan tipe signup"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if role == 'law_expert':
            serializer = LawExpertSignUpSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "Message": "Request verifikasi ahli hukum telah dibuat"
                })

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
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

