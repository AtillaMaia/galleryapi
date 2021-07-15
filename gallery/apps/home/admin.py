from django import forms
from django.contrib import admin

from .models import Post, Comments


@admin.register(Post, site=admin.site)
class PostAdmin(admin.ModelAdmin):
    pass