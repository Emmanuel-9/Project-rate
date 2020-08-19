from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    desc = models.TextField()
    image_url = models.ImageField(default='default.jpg', upload_to='project_pics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tech_used = models.CharField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk}) 


    @classmethod
    def get_all_posts(cls):
        return cls.objects.order_by('-date_posted')


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Rating(models.Model):
    rating_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]
    design = models.IntegerField(default=0, choices = rating_choices, null=True)
    usability = models.IntegerField(default=0, choices = rating_choices, null=True)
    content = models.IntegerField(default=0, choices = rating_choices, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post

    @classmethod
    def get_all_ratings(cls, post_id):
        return cls.objects.filter(post_id=post_id) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    contact = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)        