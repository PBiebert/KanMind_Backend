from django.contrib import admin
from .models import Board, Task


class BoardAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "due_date"]


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
