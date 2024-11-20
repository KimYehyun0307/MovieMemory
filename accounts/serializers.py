from rest_framework import serializers
from .models import User, KakaoUser, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    genre_1 = GenreSerializer()  # 읽기 전용을 제거하여 수정 가능하도록 설정
    genre_2 = GenreSerializer()
    genre_3 = GenreSerializer()

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'nickname', 
            'birthdate', 
            'profile_image', 
            'genre_1', 
            'genre_2', 
            'genre_3'
        ]

    def validate_nickname(self, value):
        if value and len(value) > 20:
            raise serializers.ValidationError("닉네임은 20자 이하로 설정해야 합니다.")
        return value

class KakaoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # UserSerializer를 포함시켜서 KakaoUser와 연결
    genre_1 = GenreSerializer()  # 장르 정보 수정 가능하도록 설정
    genre_2 = GenreSerializer()
    genre_3 = GenreSerializer()

    class Meta:
        model = KakaoUser
        fields = [
            'user', 
            'profile_nickname', 
            'profile_image', 
            'birthdate', 
            'genre_1', 
            'genre_2', 
            'genre_3'
        ]