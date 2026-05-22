from django.urls import path
from .views import (
    BoardView,
    BoardDetailView,
    TaskCreateView,
    CommentView,
    DeleteCommentView,
    SingleTaskView,
    AssignedToMeTasksView,
    ReviewingTasksView,
)

urlpatterns = [
    path("boards/", BoardView.as_view()),
    path("boards/<int:pk>/", BoardDetailView.as_view()),
    path("tasks/", TaskCreateView.as_view()),
    path("tasks/assigned-to-me/", AssignedToMeTasksView.as_view()),
    path("tasks/reviewing/", ReviewingTasksView.as_view()),
    path("tasks/<int:pk>/", SingleTaskView.as_view()),
    path("tasks/<int:pk>/comments/", CommentView.as_view()),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", DeleteCommentView.as_view()),
]
