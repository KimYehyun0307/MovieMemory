from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('genre/<int:genre_id>/', views.genre, name='genre'),  # 장르 URL 경로 수정
    path('search/', views.search, name='search'),
    path('memory/', views.memory, name='memory'),  # Memory 페이지 추가
    path('<str:user_nickname>/profile/', views.profile, name='profile'),
    path('<str:user_nickname>/profile/edit', views.profile_edit, name='profile_edit'),
    path('scrap_toggle/<int:movie_id>/', views.scrap_toggle, name='scrap_toggle'),
]
