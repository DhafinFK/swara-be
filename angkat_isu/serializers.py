from rest_framework import serializers
from .models import *


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = PostImage
        fields = ('image',)


class PostSerializer(serializers.ModelSerializer):
    UserId  = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects, many=False)
    
    PostId = serializers.UUIDField(source='id', read_only=True)
    Title = serializers.CharField(source='title', max_length=80)
    Text = serializers.CharField(source='text', max_length=3000) 
    Votes = serializers.IntegerField(source='like_count', read_only=True)
    Status = serializers.CharField(source='status', read_only=True)

    UserName = serializers.SerializerMethodField(method_name='get_user_name', read_only=True)
    Images = serializers.SerializerMethodField(method_name="get_post_images", read_only=True)
    LikedByUser = serializers.SerializerMethodField(method_name='get_like_flag', read_only=True)    
    Comments = serializers.SerializerMethodField(method_name='get_first_layer_comments', read_only=True)
    IsOwner = serializers.SerializerMethodField(method_name='get_is_owner', read_only=True)

    class Meta:
        model = Post
        fields = ('UserId', 'PostId', 'UserName', 'Title', 'Text', 'Images', 'Votes', 'LikedByUser', 'Comments', 'IsOwner', 'Status')

    
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

        serializer = CommentSerializer(comments, many=True)
        
        return serializer.data

    def get_user_name(self, obj):
        return obj.user.full_name.split()[0]
    
    
    def get_post_images(self, obj):
        images = obj.postimage_set.all()
        serializer = PostImageSerializer(images, many=True, context=self.context)

        return serializer.data
    
    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user == obj.user
        return False

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
    Comment = serializers.CharField(source="text")
    HasReply = serializers.SerializerMethodField(read_only=True, method_name="get_has_reply")
    UserName = serializers.SerializerMethodField(method_name='get_user_name', read_only=True)
    UserRole = serializers.SerializerMethodField(method_name='get_role', read_only=True)
    UserEmail = serializers.SerializerMethodField(method_name='get_user_email', read_only=True)
    

    class Meta:
        model = Comment
        fields = ('id', 'UserId', 'PostId', 'CommentId', 'UserName', 'UserEmail', 'UserRole', 'Comment', 'HasReply')


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
    
    def get_role(self, obj):
        return obj.user.role
    
    def get_user_email(self, obj):
        return obj.user.email