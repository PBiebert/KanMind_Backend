from django.urls import path
from .views import BoardView, BoardDetailView, TaskCreateView

urlpatterns = [
    path('boards/', BoardView.as_view()),
    path('boards/<int:pk>/', BoardDetailView.as_view()),
    path('tasks/', TaskCreateView.as_view())
]
