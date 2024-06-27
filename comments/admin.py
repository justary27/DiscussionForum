from django.contrib import admin

from comments.models import Comment, LikeComment, Reply

# Register your models here.
admin.site.register(Comment)
admin.site.register(LikeComment)
admin.site.register(Reply)