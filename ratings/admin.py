from django.contrib import admin
from .models import Post, Comment, Rating,Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Profile)