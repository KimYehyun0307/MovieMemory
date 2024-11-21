from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<str:user_name>/profile/', views.profile, name='profile'),
    path('<str:user_name>/profile/edit', views.profile_edit, name='profile_edit'),
    path('search/', views.search, name='search'),
    path('genre/<int:genre_id>/', views.genre, name='genre'),  # 장르 URL 경로 수정
]
