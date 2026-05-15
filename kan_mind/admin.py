from django.contrib import admin
from .models import Board, Task, Comment


class BoardAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "due_date"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "created_at"]


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
