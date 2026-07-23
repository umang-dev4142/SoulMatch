# Register your models here.
from django.contrib import admin
from .models import Profile
from .models import Profile, Like

admin.site.register(Profile)
admin.site.register(Like)