from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="boards")
    owner = models.ForeignKey(
        User, related_name="board_owner", on_delete=models.CASCADE)
