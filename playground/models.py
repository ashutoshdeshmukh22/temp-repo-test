from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User

import random
import uuid
import datetime
from django.utils import timezone
import pytz

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.CharField(primary_key=True, max_length=100, null=False, default='')
    limit = models.IntegerField(default=30000)
    phone = models.CharField(max_length=12, null=True)
    note = models.CharField(max_length=100, null=True)
    parent_id = models.CharField(max_length=100, null=True)

    def generate_random_code(self):
        return random.randint(10000, 99999)
    
    def create_profile(self, parent_id) -> None:
        while True:
            code = self.generate_random_code()
            if not User.objects.filter(username=code).exists():
                return f"{parent_id}{code}"
            
    
    def __str__(self):
        return self.client_id
    
    def save(self) -> None:
        return super().save()

class app_configs(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=False)
    value = models.TextField(max_length=800, null=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Convert the created_at field to 'Asia/Kolkata' timezone
        tz = pytz.timezone('Asia/Kolkata')
        self.created_at = timezone.localtime(timezone.now(), tz)
        self.updated_at = timezone.localtime(timezone.now(), tz)
        super().save(*args, **kwargs)


class Transactions(models.Model):
    transaction_id = models.CharField(primary_key=True, unique=True, editable=False, max_length=50, default="")
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    script_code = models.CharField(max_length=100, default="", null=False)
    name = models.CharField(max_length=100, default="", null=False)
    quantity = models.IntegerField(null=False)
    multiplier = models.PositiveIntegerField(null=True)
    lotSize = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=False)
    action = models.CharField(choices=[("Buy", "Buy"), ("Sell", "Sell")], max_length=5, null=False, default="Buy")
    profit_loss = models.FloatField(null=True, default=0.0)

    status_choices = ((True, 'Active'), (False, 'Closed'))
    status = models.BooleanField(choices=status_choices, default=True, null=True)
    expirydate = models.DateField(null=True)

    offerPrice = models.FloatField(default=0, null=True)
    bidPrice = models.FloatField(default=0, null=True)

    created_by = models.CharField(max_length=50, default="")
    updated_by = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def generate_unique_uuid(self):
        while True:
            uuid_value = str(uuid.uuid4())
            if Transactions.objects.filter(transaction_id=uuid_value).exists():
                continue
            return uuid_value

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_unique_uuid()
        
        tz = pytz.timezone('Asia/Kolkata')
        self.created_at = timezone.localtime(timezone.now(), tz)
        self.updated_at = timezone.localtime(timezone.now(), tz)

        super().save(*args, **kwargs)


class SquredOffTransactions(models.Model):
    transaction_id = models.CharField(primary_key=True, unique=True, editable=False, max_length=50, default="")
    parent_transaction = models.CharField(default="", null=False, max_length=255)
    client_id = models.CharField(max_length=50, default="")
    script_code = models.CharField(max_length=100, default="", null=False)
    name = models.CharField(max_length=100, default="", null=False)
    quantity = models.IntegerField(null=False)
    multiplier = models.PositiveIntegerField(null=True)
    lotSize = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=False)
    action = models.CharField(choices=[("Buy", "Buy"), ("Sell", "Sell")], max_length=5, null=False, default="Buy")
    profit_loss = models.FloatField(null=True, default=0.0)
    expirydate = models.DateField(null=True)

    offerPrice = models.PositiveIntegerField(default=0, null=True)
    bidPrice = models.PositiveIntegerField(default=0, null=True)

    created_by = models.CharField(max_length=50, default="")
    updated_by = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def generate_unique_uuid(self):
        while True:
            uuid_value = str(uuid.uuid4())
            if SquredOffTransactions.objects.filter(transaction_id=uuid_value).exists():
                continue
            return uuid_value

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_unique_uuid()
        
        tz = pytz.timezone('Asia/Kolkata')
        self.created_at = timezone.localtime(timezone.now(), tz)
        self.updated_at = timezone.localtime(timezone.now(), tz)
        super().save(*args, **kwargs)


class token_log(models.Model):
    id = models.AutoField(primary_key=True)
    request_url = models.CharField(max_length=100, null=False)
    encrypted_token = models.CharField(max_length=300, null=False)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        tz = pytz.timezone('Asia/Kolkata')
        self.created_at = timezone.localtime(timezone.now(), tz)
        super().save(*args, **kwargs)

class Scripts(models.Model):

    id = models.AutoField(primary_key=True)
    script_code = models.PositiveIntegerField(null=False, default=0)
    tradingSymbol = models.CharField(max_length=100, null=False, default="")
    lotSize = models.PositiveIntegerField(null=False, default=1)
    multiplier = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    expiryDate = models.DateField(null=False)
    optionType = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        
        tz = pytz.timezone('Asia/Kolkata')
        self.created_at = timezone.localtime(timezone.now(), tz)
        self.updated_at = timezone.localtime(timezone.now(), tz)
        super().save(*args, **kwargs)

