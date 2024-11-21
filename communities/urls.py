from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.main_community, name='main_community'),
    path('<str:movie_title>/board/', views.board, name='movieboard'),
    path('<str:movie_title>/board/<int:post_num>/', views.post, name='post'),
    path('<str:movie_title>/board/<int:post_num>/edit/', views.post_edit, name='post_edit'),
    path('<str:movie_title>/board/<int:post_num>/delete/', views.post_delete, name='post_delete'),  # 영화 게시물 삭제
    path('bamboo/', views.bamboo, name='bamboo'),
    path('bamboo/<int:post_num>/', views.bamboo_post, name='bamboo_post'),
    path('bamboo/<int:post_num>/edit/', views.bamboo_post_edit, name='bamboo_post_edit'),
    path('bamboo/<int:post_num>/delete/', views.bamboo_post_delete, name='bamboo_post_delete'),  # 대나무숲 게시물 삭제
    path('events/', views.event, name='event'),
    path('events/<str:eventname>/', views.event_section, name='event_section'),
    path('events/<str:eventname>/participate/', views.event_participation, name='event_participation'),  # 이벤트 참여
]
