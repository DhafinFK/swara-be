from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import LawExpertSignUp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    FullName = serializers.CharField(source='full_name', required=True)
    Email = serializers.EmailField(source='email', required=True)
    Password = serializers.CharField(source='password', write_only=True, required=True)
    SignUpType = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='role', required=True)
    Certificate = serializers.URLField(source='lawyer_certificate', required=False, allow_blank=False, allow_null=True)

    class Meta:
        model = User
        fields = ('FullName', 'Email', 'Password', 'SignUpType', 'Certificate')


    def validate(self, data):

        role = data.get('role')
        certificate = data.get('law_certificate', None)

        if role == 'law_expert' and not certificate:
            raise serializers.ValidationError("Ahli hukum harus menyertakan sertifikat!")
        if role == 'regular_user' and certificate:
            raise serializers.ValidationError("Pengguna biasa tidak boleh upload sertifikat!")

        return data

    def validate_Email(self, value):
        email = value
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email sudah dipakai!")
        
        return value
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    

class LawExpertSignUpSerializer(serializers.ModelSerializer):

    FullName = serializers.CharField(source='full_name', required=True)
    Email = serializers.EmailField(source='email', required=True)
    Password = serializers.CharField(source='password', write_only=True, required=True)
    Certificate = serializers.URLField(source='law_certificate')

    class Meta:
        model = LawExpertSignUp
        fields = ('Email', 'FullName', 'Password', 'Certificate')
        write_only = ('password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)