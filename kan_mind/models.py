from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="boards")
    owner = models.ForeignKey(
        User, related_name="board_owner", on_delete=models.CASCADE)


class Task(models.Model):
    STATUS_CHOICES = (
        ('to-do', 'to-do'),
        ('in-progress', 'in-progress'),
        ('review', 'review'),
        ('done', 'done'),
    )

    PRIORITY_CHOICES = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high')
    )

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='creator')
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='assignee')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='reviewer')
    due_date = models.DateField()


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
