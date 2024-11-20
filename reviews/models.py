from django.db import models
from django.conf import settings
from movies.models import Movie

class Review(models.Model):
    # 영화와 작성자를 ForeignKey로 연결
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)       # 영화 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자

    # 리뷰 내용
    content = models.TextField()
    rating = models.IntegerField(default=5)  # 1~5점 사이의 평가 (기본값: 5점)

    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시간

    def __str__(self):
        return f'{self.movie.title} - {self.user.username}의 리뷰'


# Create your models here.
