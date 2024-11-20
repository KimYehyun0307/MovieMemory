from django.contrib import admin
from .models import User, KakaoUser, Genre

# Register your models here.
admin.site.register(User)
admin.site.register(KakaoUser)
admin.site.register(Genre)