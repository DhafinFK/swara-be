from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *


class AngkatIsuAPI(APIView):

    parser_classes = [JSONParser]

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
        self.permission_classes = [IsAuthenticated]

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
        
