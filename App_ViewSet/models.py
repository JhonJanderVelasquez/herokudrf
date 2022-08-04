from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=250)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.title