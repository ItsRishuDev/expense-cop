from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class userDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    credential = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.FloatField()
    current_balance = models.FloatField()

    def __str__(self):
        return self.credential.first_name

class transaction(models.Model):
    action_type = (
        ('0', 'Deposite'),
        ('1', 'Withdrawal')
    )
    transaction_id = models.AutoField(primary_key=True)
    transaction_name = models.CharField(max_length=1000)
    transaction_type = models.CharField(max_length=10, choices=action_type)
    transaction_amaount = models.FloatField()
    credential = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.credential.first_name