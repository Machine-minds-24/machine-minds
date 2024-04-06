from django.db import models

class DreamApp(models.Model):
    description = models.TextField()
    feature_list = models.TextField(blank=True, null=True)