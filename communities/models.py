from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from movies.models import Movie
import random
import string


# 영화 후기 모델
class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    nickname = models.CharField(max_length=20)  # 게시글에 표시될 닉네임
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_comment_enabled = models.BooleanField(default=True)  # 댓글 허용 여부
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)  # 1~5점 평가
    liked_users = models.ManyToManyField(User, related_name="liked_reviews", blank=True)
    image = models.ImageField(upload_to='movie_reviews/', blank=True, null=True)  # 영화 후기 이미지

    def __str__(self):
        return f"{self.title} ({self.nickname})"

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('평점은 1에서 5 사이여야 합니다.')



# 대나무숲 모델
class BambooPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bamboo_posts")
    anonymous_name = models.CharField(max_length=20)  # 익명 + 랜덤 숫자
    title = models.CharField(max_length=100)  # 제목 필드 추가
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='bamboo_posts/', blank=True, null=True)  # 대나무숲 이미지
    liked_users = models.ManyToManyField(User, related_name="liked_bamboo_posts", blank=True)  # 좋아요 사용자

    def __str__(self):
        return f"Anonymous ({self.anonymous_name}) - {self.title}"  # 제목도 반환하도록 수정
    
    def save(self, *args, **kwargs):
        if not self.anonymous_name:
            self.anonymous_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 랜덤 이름
        super().save(*args, **kwargs)


# 댓글 모델
class Comment(models.Model):
    # 리뷰 또는 대나무숲 게시물과 연결
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    post = models.ForeignKey(BambooPost, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    
    # 댓글 작성자 (영화 게시판에서는 닉네임 사용, 대나무숲에서는 익명 이름 사용)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)  # User 모델 사용
    nickname = models.CharField(max_length=20, null=True, blank=True)  # 영화 게시판에서 사용
    anonymous_name = models.CharField(max_length=20, null=True, blank=True)  # 대나무숲에서만 사용
    
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 댓글 수정일

    is_reply = models.BooleanField(default=False)  # 대댓글 여부
    image = models.ImageField(upload_to='comments/', blank=True, null=True)  # 댓글 이미지

    def save(self, *args, **kwargs):
        # 대나무숲 댓글에는 anonymous_name을 랜덤으로 생성
        if self.post and not self.anonymous_name:
            self.anonymous_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 랜덤 이름

        # 영화 리뷰 댓글에는 nickname만 사용
        if self.review and not self.nickname:
            if self.user:
                self.nickname = self.user.nickname  # 댓글 작성자가 있다면 해당 사용자의 nickname으로 설정

        super().save(*args, **kwargs)

    def __str__(self):
        # 익명 댓글과 일반 댓글을 구분하여 반환
        if self.anonymous_name:
            return f"Comment by Anonymous ({self.anonymous_name})"
        return f"Comment by {self.nickname}"

# 대댓글 모델
class CommentReply(models.Model):
    # 댓글과 연결
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")

    # 대댓글 작성자 (댓글 작성자와 동일)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    nickname = models.CharField(max_length=20, null=True, blank=True)  # 대댓글 작성자 닉네임
    anonymous_name = models.CharField(max_length=20, null=True, blank=True)  # 대나무숲 대댓글에서 익명 사용

    content = models.TextField()  # 대댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 대댓글 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 대댓글 수정일
    image = models.ImageField(upload_to='replies/', blank=True, null=True)  # 대댓글 이미지

    def save(self, *args, **kwargs):
        # 대댓글이 연결된 댓글이 대나무숲 게시물인 경우
        if self.comment.post and not self.nickname:
            # 대나무숲 대댓글에는 anonymous_name을 랜덤으로 생성
            self.anonymous_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 랜덤 이름 생성
        elif self.comment.review and not self.nickname:
            # 영화 리뷰 대댓글에는 nickname을 설정
            if self.user:
                self.nickname = self.user.nickname  # 댓글 작성자가 있다면 해당 사용자의 nickname으로 설정
            self.anonymous_name = ''  # 대댓글이 영화 리뷰에 속하면 익명 이름을 비워둠

        super().save(*args, **kwargs)

    def __str__(self):
        if self.anonymous_name:
            return f"Reply by Anonymous ({self.anonymous_name})"
        return f"Reply by {self.nickname}"


# 영화 게시판에서 좋아요 모델
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name='like_set', null=True, blank=True)  # MovieReview와 연결
    post = models.ForeignKey(BambooPost, on_delete=models.CASCADE, related_name='like_set', null=True, blank=True)  # BambooPost와 연결

    def __str__(self):
        return f"Like from {self.user} on {self.review.title if self.review else self.post.content}"

    class Meta:
        unique_together = ('user', 'review', 'post')

class ScreeningSchedule(models.Model):
    movie_title = models.CharField(max_length=255)  # 영화 제목을 저장할 컬럼
    screening_date = models.DateField()

    def __str__(self):
        return f"{self.movie_title} at ({self.screening_date})"