from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
import requests
from django.conf import settings

class Genre(models.Model):
    id = models.PositiveIntegerField(primary_key=True)  # id를 primary_key로 설정하여 fixtures에서 수동 관리 가능
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="닉네임은 20자 이하로 설정해야 합니다."
    )
    birthdate = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile/',
        default='profile/default.png',
        blank=True,
        null=True
    )
    genre_1 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_1')
    genre_2 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_2')
    genre_3 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_3')

    # 공개 범위 필드 추가
    is_nickname_public = models.BooleanField(default=True)  # 닉네임 공개 여부
    is_birthdate_public = models.BooleanField(default=True)  # 생년월일 공개 여부
    is_genre_public = models.BooleanField(default=True)  # 좋아하는 장르 공개 여부
    is_reviews_public = models.BooleanField(default=True)  # detail 댓글 목록 공개 여부
    is_post_public = models.BooleanField(default=True) # 영화게시판 작성글 목록 공개 여부
    is_comments_public = models.BooleanField(default=True) # 댓글, 대댓글 목록 공개 여부
    # visited_at = models.DateTimeField(null=True, blank=True) # 마지막 접속 시간
    
    def save(self, *args, **kwargs):
        # 닉네임 자동 생성
        if not self.nickname:
            base_nickname = self.username
            unique_id = get_random_string(length=6)  # 6자리 랜덤 문자열
            self.nickname = f"{base_nickname}{unique_id}"[:20]  # 닉네임은 20자 이하로 제한
        super().save(*args, **kwargs)


class KakaoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kakao_user')
    profile_nickname = models.CharField(max_length=50, blank=True, null=True)  # 카카오에서 제공하는 프로필 닉네임
    profile_image = models.URLField(blank=True, null=True)  # 카카오에서 제공하는 프로필 이미지 URL

    # 카카오에서 수집한 생년월일 정보 (프로젝트에서 설정된 것과 구별)
    birthdate = models.DateField(blank=True, null=True)

    # 영화 장르 정보 (프로젝트에서 관리)
    genre_1 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_1')
    genre_2 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_2')
    genre_3 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_3')

    def __str__(self):
        return f"KakaoUser: {self.profile_nickname or self.user.username}"
