from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin): # created admin to manage blog posts and see if they are reaching the database
    model = Blog
admin.site.register(Blog, BlogAdmin)