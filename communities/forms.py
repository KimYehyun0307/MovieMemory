from django import forms
from .models import MovieReview, Comment, CommentReply, BambooPost, EventParticipation


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['title', 'content', 'rating', 'is_comment_enabled', 'image']  # image 필드 추가


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'is_reply', 'image']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['content', 'image']


class BambooPostForm(forms.ModelForm):
    class Meta:
        model = BambooPost
        fields = ['title', 'content', 'image']  # image 필드 추가


class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['event']
