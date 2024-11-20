from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('create/<int:movie_id>/', views.create_review, name='create_review'),
    path('update/<int:review_id>/', views.update_review, name='update_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('comment/create/<int:review_id>/', views.create_comment, name='create_comment'),
    path('add_comment/<int:review_id>/', views.add_comment, name='add_comment'),
]
