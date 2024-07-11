from .models import *

class LikeServices:
    
    def increment(self, post_id):
        post = Post.objects.get(id=post_id)
        post.like_count += 1
        post.save()

    def decrement(self, post_id):
        post = Post.objects.get(id=post_id)
        post.like_count -= 1
        post.save()