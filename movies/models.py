from django.db import models
from django.contrib.auth.models import User
from accounts.models import User

class Movie(models.Model):
    # TMDB에서 제공하는 영화 고유 ID
    tmdb_id = models.IntegerField(unique=True)  
    title = models.CharField(max_length=200)     # 영화 제목
    overview = models.TextField(blank=True)      # 영화 줄거리
    release_date = models.DateField(blank=True, null=True)  # 개봉일
    poster_path = models.CharField(max_length=200, blank=True)  # 포스터 이미지 경로
    
    def __str__(self):
        return self.title

