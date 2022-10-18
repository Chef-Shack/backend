from djongo import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Recipe(models.Model):
    recipe_title = models.TextField(max_length=100)
    recipe_description = models.TextField(max_length=250)
    pub_date = models.DateTimeField(datetime.datetime.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}: {self.recipe_title}'
