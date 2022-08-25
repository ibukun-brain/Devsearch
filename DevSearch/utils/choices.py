from django.db import models

class Votes(models.TextChoices):
        UP = "up", "Up vote"
        DOWN = "down", "Up down"