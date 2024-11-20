from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, KakaoUser

class CustomUserCreationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'profile_image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'birthdate', 'profile_image', 'genre_1', 'genre_2', 'genre_3']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and len(nickname) > 20:
            raise forms.ValidationError("닉네임은 20자 이하로 설정해야 합니다.")
        return nickname

class KakaoUserForm(forms.ModelForm):
    class Meta:
        model = KakaoUser
        fields = ['profile_nickname', 'profile_image', 'birthdate', 'genre_1', 'genre_2', 'genre_3']
