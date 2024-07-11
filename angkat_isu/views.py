from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from .permissions import *
from .services import *


class AngkatIsuAPI(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        top_posts = Post.objects.all().order_by("-like_count")[:4]  

        context = {
            'request': request,
            'get_detail': False
        }

        serializer = PostSerializer(top_posts, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        self.permission_classes = [IsAuthenticated]

        data = request.data.copy()
        data["UserId"] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.permission_classes = [IsAuthenticated, IsOwner]

        try:
            post_id = request.data.get("PostId")
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                "Message": "Isu tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.check_permissions(request)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PostImageView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                "Message": "Post Tidak Ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, post)

        images = request.FILES.getlist('images')

        for image in images:
            post_image = PostImage.objects.create(post=post, image=image)

        return Response({
            "Message": "Berhasil Upload Gambar"
        }, status=status.HTTP_201_CREATED)


class PostDetail(APIView):
    parser_classes = [JSONParser]
        
    def get(self, request, post_id):
        try:
            target_post = Post.objects.get(id=post_id)
            context = {
                'request': request,
                'get_detail': True
            }

            serializer = PostSerializer(target_post, context=context)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({
                "Message": "Isu tidak ditemukan"
            })
        

class LikeUnlikeAPI(APIView):

    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    like_service = LikeServices()

    def post(self, request):
        user_id = request.user.id
        post_id = request.data.get("PostId")

        like_instance = Like.objects.filter(user__id=user_id, post__id=post_id)

        if like_instance:
            return Response({
                'Message': 'User Sudah Like'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['UserId'] = user_id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            self.like_service.increment(post_id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.user.id
        post_id = request.data.get("PostId")

        like_instance = Like.objects.filter(user__id=user_id, post__id=post_id)

        if like_instance:
            like_instance.delete()
            self.like_service.decrement(post_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({
            "Message": "User Belum Like"
        }, status=status.HTTP_400_BAD_REQUEST)


class CommentAPI(APIView):

    parser_classes = [JSONParser]
    
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        data = request.data.copy()
        data["UserId"] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.permission_classes = [IsAuthenticated, IsOwner]
        comment_id = request.data.get("CommentId")
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({
                "Message": "Komentar Tidak Ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.check_permissions(request)
        self.check_object_permissions(request, comment)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentPostList(APIView):

    parser_classes = [JSONParser]

    def get(self, request, post_id):      
        comments = Comment.objects.filter(post__id=post_id, reply_comment__isnull=True)[:10]
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)
    

class CommentReplyList(APIView):

   parser_classes = [JSONParser]

   def get(self, request, comment_id):
      comments = Comment.objects.filter(reply_comment=comment_id)
      serializer = CommentSerializer(comments, many=True)

      return Response(serializer.data)
