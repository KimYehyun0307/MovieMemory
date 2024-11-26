from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.main_community, name='main_community'),
    path('search_movie/', views.search_movie, name='search_movie'),
    path('<str:movie_title>/board/', views.board, name='movieboard'),
    path('<str:movie_title>/board/<int:post_num>/', views.post, name='post'),
    path('<str:movie_title>/board/<int:post_num>/like/', views.like_post, name='like_post'),
    path('<str:movie_title>/board/create/', views.post_create, name='post_create'),
    path('<str:movie_title>/board/<int:post_num>/edit/', views.post_edit, name='post_edit'),
    path('<str:movie_title>/board/<int:post_num>/delete/', views.post_delete, name='post_delete'), 
    path('<str:movie_title>/board/<int:post_num>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<str:movie_title>/board/<int:post_num>/comment/<int:comment_id>/reply/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('bamboo/', views.bamboo, name='bamboo'),
    path('bamboo/create/', views.bamboo_post_create, name='bamboo_post_create'),
    path('bamboo/<int:post_num>/', views.bamboo_post, name='bamboo_post'),
    path('bamboo/<int:post_num>/like/', views.like_post_bamboo, name='like_post_bamboo'),
    path('bamboo/<int:post_num>/edit/', views.bamboo_post_edit, name='bamboo_post_edit'),
    path('bamboo/<int:post_num>/delete/', views.bamboo_post_delete, name='bamboo_post_delete'),
    path('bamboo/<int:post_num>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('bamboo/<int:post_num>/comment/<int:comment_id>/reply/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('events/', views.event, name='event'),
    path('events/<str:eventname>/', views.event_section, name='event_section'),
    path('events/<str:eventname>/create/', views.event_create, name='event_create'), 
    path('events/<str:eventname>/participate/', views.event_participation, name='event_participation'), 
]
