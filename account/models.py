
from django.db import models
from django.contrib.auth.models import User
    

class Deposit(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_account')
    account_no=models.IntegerField(unique=True, default=1000)
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    balance_after_tranjections = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return str(self.account_no)
