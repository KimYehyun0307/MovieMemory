from rest_framework import serializers
from .models import Movie, MovieReview, Comment, BambooPost, Event, EventParticipation, ScreeningSchedule


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'tmdb_id', 'release_date', 'poster_image']  # poster_image 필드 포함


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = ['id', 'movie', 'user', 'nickname', 'title', 'content', 'created_at', 'updated_at', 'is_comment_enabled', 'rating', 'likes', 'image']  # image 필드 추가


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'nickname', 'content', 'created_at', 'updated_at', 'is_reply', 'image']  # image 필드 추가


class BambooPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BambooPost
        fields = ['id', 'user', 'anonymous_name', 'content', 'created_at', 'updated_at', 'image']  # image 필드 추가


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'is_active', 'image']  # image 필드 추가


class EventParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipation
        fields = ['id', 'event', 'user', 'score', 'created_at']


class ScreeningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningSchedule
        fields = ['id', 'movie', 'cinema_name', 'location', 'screening_date', 'screening_time']
