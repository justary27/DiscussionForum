from django.contrib import admin

from discussions.models import  Discussion,  Like

# Register your models here.
admin.site.register(Discussion)
admin.site.register(Like)
