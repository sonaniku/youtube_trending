from django.db import models
from datetime import datetime
# Create your models here.

class LatestUpdated(models.Model):
    latest_updated_date = models.DateTimeField(default=datetime.today(), primary_key=True)