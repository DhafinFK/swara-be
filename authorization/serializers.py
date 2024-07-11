from django.contrib.auth import get_user_model
from rest_framework import serializers

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
    