from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    # Podem definir el maxim de caracters de username
    username = models.CharField(max_length=32, primary_key=True)
    description = models.TextField(default="")
    cover = models.ImageField(default="")
    avatar = models.ImageField(default="")
    email = models.EmailField(unique=True)


