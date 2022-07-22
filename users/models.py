from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=200, unique=True)
    password      = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=50)
    birthday      = models.DateField(null=True)

    class Meta:
        db_table = 'users'