from django.db import models
from .user import User


class Thread(models.Model):
    # Automaticament, si no s'especifica, django genera un id (int) com a PK
    # Rang dels likes [0-2147483647]
    num_likes = models.PositiveIntegerField(default=0)
    # En cas que l'author associat s'elimini, tots el threads seus s'elimines
    author = models.ForeignKey(User, on_delete=models.CASCADE,default='default_user')
    title = models.TextField(max_length=255,default='')
    body = models.TextField(max_length=35000,null=True)
    url = models.TextField(max_length=35000,default='')

