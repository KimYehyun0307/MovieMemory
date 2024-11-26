from django import forms
from .models import MovieReview, Comment, CommentReply, BambooPost


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['title', 'content', 'rating', 'is_comment_enabled', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '영화 제목'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요', 'rows': 4}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'is_comment_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        # 디폴트 값을 5로 설정
        initial = {
            'rating': 5,  # rating 필드의 기본값을 5로 설정
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'is_reply', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '댓글을 작성하세요', 'rows': 3}),
            'is_reply': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 'is_reply' 필드의 레이블을 '대댓글 허용'으로 변경
        self.fields['is_reply'].label = '대댓글 허용'


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '대댓글을 작성하세요', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class BambooPostForm(forms.ModelForm):
    class Meta:
        model = BambooPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '대나무숲 제목'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }