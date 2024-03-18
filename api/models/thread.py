from django.db import models

from .user import User


class Thread(models.Model):
    # Automaticament, si no s'especifica, django genera un id (int) com a PK
    # Rang dels likes [0-2147483647]
    num_likes = models.PositiveIntegerField(default=0)
    # En cas que l'author associat s'elimini, tots el threads seus s'elimines
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
