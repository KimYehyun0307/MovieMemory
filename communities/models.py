from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from movies.models import Movie
import random
import string


# 영화 후기 모델
class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    nickname = models.CharField(max_length=20)  # 게시글에 표시될 닉네임
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_comment_enabled = models.BooleanField(default=True)  # 댓글 허용 여부
    rating = models.PositiveSmallIntegerField(default=5)  # 1~5점 평가
    likes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/movie_reviews/', blank=True, null=True)  # 영화 후기 이미지

    def __str__(self):
        return f"{self.title} ({self.nickname})"
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('평점은 1에서 5 사이여야 합니다.')


# 영화 게시판에서 좋아요 모델
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name='like_set')  # related_name을 추가

    def __str__(self):
        return f"Like from {self.user} on {self.review.title}"
    
    class Meta:
        unique_together = ('user', 'review')  # 같은 리뷰에 대해 여러 번 좋아요를 누를 수 없도록 설정


# 댓글 모델
class Comment(models.Model):
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    post = models.ForeignKey('BambooPost', on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    
    # 영화 게시판에서는 nickname 사용, 대나무숲에서는 익명 이름 사용
    nickname = models.CharField(max_length=20, null=True, blank=True)  # 영화 게시판에서 사용
    anonymous_name = models.CharField(max_length=20, null=True, blank=True)  # 대나무숲에서만 사용
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 댓글이 대댓글인 경우를 위한 필드
    is_reply = models.BooleanField(default=False)  # 대댓글 여부
    # 댓글에 이미지를 첨부할 수 있는 필드
    image = models.ImageField(upload_to='media/comments/', blank=True, null=True)  # 댓글 이미지

    def save(self, *args, **kwargs):
        # 대나무숲 댓글에는 anonymous_name을 랜덤으로 생성
        if self.post and not self.anonymous_name:
            self.anonymous_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 랜덤 이름
        # 영화 리뷰 댓글에는 nickname만 사용
        if self.review and not self.nickname:
            self.nickname = self.user.nickname  # 댓글 작성자가 있다면 해당 사용자의 nickname으로 설정
        super().save(*args, **kwargs)

    def __str__(self):
        if self.anonymous_name:
            return f"Comment by Anonymous ({self.anonymous_name})"
        return f"Comment by {self.nickname}"




# 대나무숲 모델
class BambooPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bamboo_posts")
    anonymous_name = models.CharField(max_length=20)  # 익명 + 랜덤 숫자
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/bamboo_posts/', blank=True, null=True)  # 대나무숲 이미지

    def __str__(self):
        return f"Anonymous ({self.anonymous_name})"
    
    def save(self, *args, **kwargs):
        if not self.anonymous_name:
            self.anonymous_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 랜덤 이름
        super().save(*args, **kwargs)


# 이벤트 모델
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/events/', blank=True, null=True)  # 이벤트 이미지

    def __str__(self):
        return self.name


# 이벤트 참여 모델
class EventParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_participations")
    score = models.PositiveIntegerField(default=0)  # 퀴즈 등 점수 기록
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} in {self.event.name}"


class ScreeningSchedule(models.Model):
    movie_title = models.CharField(max_length=255)  # 영화 제목을 저장할 컬럼
    screening_date = models.DateField()

    def __str__(self):
        return f"{self.movie_title} at {self.cinema_name} ({self.screening_date})"