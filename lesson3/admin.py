from django.contrib import admin

# Register your models here.
from lesson3.models import News, Comment

admin.site.register(News)
admin.site.register(Comment)