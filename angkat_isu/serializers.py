from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    UserId  = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects, many=False)
    
    PostId = serializers.UUIDField(source='id', read_only=True)
    Title = serializers.CharField(source='title', max_length=80)
    Text = serializers.CharField(source='text', max_length=3000) 
    Votes = serializers.IntegerField(source='like_count', read_only=True)

    UserName = serializers.SerializerMethodField(method_name='get_user_name', read_only=True)
    LikedByUser = serializers.SerializerMethodField(method_name='get_like_flag')    
    Comments = serializers.SerializerMethodField(method_name='get_first_layer_comments')

    class Meta:
        model = Post
        fields = ('UserId', 'PostId', 'UserName', 'Title', 'Text', 'Votes', 'LikedByUser', 'Comments')

    
    def get_like_flag(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False
    
    def get_first_layer_comments(self, obj):
        type_detail = self.context.get('get_detail', None)
        comments = Comment.objects.filter(post=obj, reply_comment__isnull=True)

        if not comments.exists():
            return None

        if not type_detail:
            serializer = CommentSerializer(comments[0])
        else:
            serializer = CommentSerializer(comments, many=True)
        
        return serializer.data

    def get_user_name(self, obj):
        return obj.user.full_name.split()[0]
    

class LikeSerializer(serializers.ModelSerializer):
    UserId = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects, many=False, write_only=True)
    PostId = serializers.PrimaryKeyRelatedField(source="post", queryset=Post.objects, many=False)

    class Meta:
        model = Like    
        fields = ('UserId', 'PostId')


class CommentSerializer(serializers.ModelSerializer):
    UserId = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects, many=False, write_only=True)
    PostId = serializers.PrimaryKeyRelatedField(source="post", queryset=Post.objects, many=False)
    CommentId = serializers.PrimaryKeyRelatedField(source="reply_comment", queryset=Comment.objects, required=False, many=False)
    UserName = serializers.SerializerMethodField(method_name='get_user_name', read_only=True)
    Comment = serializers.CharField(source="text")
    HasReply = serializers.SerializerMethodField(read_only=True, method_name="get_has_reply")

    class Meta:
        model = Comment
        fields = ('id', 'UserId', 'PostId', 'CommentId', 'UserName', 'Comment', 'HasReply')


    def validate_CommentId(self, value):

        comment_id = value.id

        if comment_id:
            target_comment = Comment.objects.get(id=comment_id)
            if target_comment.reply_comment:
                raise serializers.ValidationError("Cannot reply on comment reply")
        
        return value
    
    def get_user_name(self, obj):
        return obj.user.full_name.split()[0]
    
    def get_has_reply(self, obj):
        return Comment.objects.filter(reply_comment=obj).exists()