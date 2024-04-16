from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
# Create your models here.


class Expense(models.Model):
    creator = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    amount = models.IntegerField()
