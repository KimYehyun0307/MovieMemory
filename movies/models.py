from django.db import models

class Genres(models.Model):
    name = models.CharField(max_length=100)
    tmdb_id = models.IntegerField(unique=True)  # TMDB에서 제공하는 장르 ID 추가

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # TMDB에서 제공하는 영화 고유 ID
    title = models.CharField(max_length=200)     # 영화 제목
    overview = models.TextField(blank=True)      # 영화 줄거리
    release_date = models.DateField(blank=True, null=True)  # 개봉일
    poster_path = models.CharField(max_length=200, blank=True)  # 포스터 이미지 경로
    genres = models.ManyToManyField(Genres)  # 여러 장르와 연결된 관계

    def __str__(self):
        return self.title

