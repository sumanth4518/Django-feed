from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('post/new/', views.post_create_view, name='post_create'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete_view, name='post_delete'),
]
