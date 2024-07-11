from django.db import models
from authorization.models import User
from core.models import UUIDBaseModel


def upload_to_path(instance, filename):
    return f'images/{instance.post.id}/{filename}'


class Post(UUIDBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    title = models.TextField(blank=False, max_length=80)

    STATUS_CHOICES = (
        ('pendaftaran', 'Pendaftaran'),
        ('pemeriksaan_berkas', 'Pemeriksaan Berkas'),
        ('bayar_penjar_perkara', 'Bayar Panjar Perkara'),
        ('panggilan_sidang', 'Panggilan Sidang'),
        ('proses_persidangan', 'Proses Persidangan'),
        ('putusan', 'Putusan')
    )

    like_count = models.PositiveBigIntegerField(default=0)    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendaftaran')

    def __str__(self):
        return self.title
    

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_path)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(PostImage, self).delete(*args, **kwargs)
    

class Like(UUIDBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(UUIDBaseModel.Meta):
        unique_together = (("post", "user"),)
    

class Comment(UUIDBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_comment = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)


