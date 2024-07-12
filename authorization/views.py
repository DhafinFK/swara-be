from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings


User = get_user_model()


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
                serializer.save()
                return Response({
                    "Message": "Request verifikasi ahli hukum telah dibuat"
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                firstname = user.full_name.split()[0]
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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


class GoogleLogin(APIView):
    def post(self, request):
        credential = request.data.get('credential')
        
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
            
            # Check if the token is issued to your client ID
            if idinfo['aud'] != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
                raise ValueError('Could not verify audience.')

            # Get user info
            email = idinfo['email']
            full_name = idinfo.get('name')
            google_id = idinfo['sub']

            # Find or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': full_name,
                }
            )

            if created:
                user.set_unusable_password()  # or set a default password if required
                user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Get tokens for the user
            tokens = get_tokens_for_user(user)

            return Response({
                'message': 'User authenticated successfully.',
                'tokens': tokens['access']
            }, status=status.HTTP_200_OK)
        

        except ValueError as e:
            # Invalid token
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Other unexpected errors
            return Response({'error': 'An error occurred while authenticating.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)