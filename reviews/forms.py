from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']  # content와 rating만 입력받음

        # rating 필드에 대한 입력 제한
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'content': '리뷰',
            'rating': '점수',
        }
