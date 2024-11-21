from django import forms
from .models import MovieReview, Comment, BambooPost, EventParticipation


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['movie', 'title', 'content', 'rating', 'is_comment_enabled', 'image']  # image 필드 추가


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['review', 'content', 'is_reply', 'image']  # image 필드 추가


class BambooPostForm(forms.ModelForm):
    class Meta:
        model = BambooPost
        fields = ['content', 'image']  # image 필드 추가


class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['event']
