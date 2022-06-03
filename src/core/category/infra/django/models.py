from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
