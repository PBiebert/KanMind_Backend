from django.urls import path
from .views import BoardView, BoardDetailView, TaskCreateView, CommentView

urlpatterns = [
    path('boards/', BoardView.as_view()),
    path('boards/<int:pk>/', BoardDetailView.as_view()),
    path('tasks/', TaskCreateView.as_view()),
    path('tasks/<int:pk>/comments', CommentView.as_view()),
]
