from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class Genre(models.Model):
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
        default='images/default.png',
        blank=True,
        null=True
    )
    genre_1 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_1')
    genre_2 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_2')
    genre_3 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='favorite_users_3')

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

    # 프로젝트에서 받는 생년월일 정보
    birthdate = models.DateField(blank=True, null=True)

    # 영화 장르 정보 (프로젝트에서 관리)
    genre_1 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_1')
    genre_2 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_2')
    genre_3 = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name='kakao_favorite_users_3')

    def __str__(self):
        return f"KakaoUser: {self.profile_nickname or self.user.username}"
