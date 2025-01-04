from django.contrib import admin

from boostlab_posts.models import LikedPost, Post, Reply,Tag,Comment,LikedComment,LikedReply

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikedReply)