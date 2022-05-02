from django.contrib import admin
from .models import Comment, Notification, Post,UserProfile

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Notification)
