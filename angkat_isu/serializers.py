from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    UserId  = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects, many=False)
    
    PostId = serializers.UUIDField(source='id', read_only=True)
    Title = serializers.CharField(source='title', max_length=80)
    Text = serializers.CharField(source='text', max_length=3000) 
    Votes = serializers.IntegerField(source='like_count', read_only=True)

    UserName = serializers.SerializerMethodField(method_name='get_user_name', read_only=True)

    class Meta:
        model = Post
        fields = ('UserId', 'PostId', 'UserName', 'Title', 'Text', 'Votes',)

    
    def get_user_name(self, obj):
        return obj.user.full_name.split()[0]