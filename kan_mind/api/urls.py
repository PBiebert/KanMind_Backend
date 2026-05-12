from django.urls import path
from .views import BoardView, BoardDetailView

urlpatterns = [
    path('boards/', BoardView.as_view()),
    path('boards/<int:pk>/', BoardDetailView.as_view())
]
