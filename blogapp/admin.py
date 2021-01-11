from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post,Contact,BlogComment

admin.site.register((Post, BlogComment))
admin.site.register(Contact)
