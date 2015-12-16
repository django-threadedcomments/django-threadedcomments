from datetime import datetime

from django.db import models


class Person(models.Model):
    """
    This model is simply used by this application's test suite as a model to
    which to attach comments.
    """
    name = models.CharField(max_length=5)
    is_public = models.BooleanField(default=True)
    date = models.DateTimeField(default=datetime.now)
