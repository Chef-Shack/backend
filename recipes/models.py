from djongo import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    recipe_title = models.TextField(max_length=100)
    recipe_description = models.TextField(max_length=250)
    pub_date = models.DateTimeField(auto_now=True, blank=True)
    author = models.TextField()
    category = models.TextField()
    image = models.TextField()
    likes = models.IntegerField()
    ingredients = models.JSONField()
    procedure = models.JSONField()

    def __str__(self):
        return f'{self.author.username}: {self.recipe_title}'
