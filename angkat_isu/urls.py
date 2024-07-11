from django.urls import path
from .views import *

app_name = 'angkat_isu'

urlpatterns = [
    path('', AngkatIsuAPI.as_view(), name="angkat-isu"),
    path('upload/<str:post_id>/', PostImageView.as_view(), name="upload-image"),
    path('detail/<str:post_id>/', PostDetail.as_view(), name="post-detail"),
    path('like/', LikeUnlikeAPI.as_view(),name="like"),
    path('comment/', CommentAPI.as_view(), name='comment'),
    path('comment/post/<str:post_id>/', CommentPostList.as_view(), name="post-comment"),
    path('comment/reply/<str:comment_id>/', CommentReplyList.as_view(), name="reply-coment"),
]