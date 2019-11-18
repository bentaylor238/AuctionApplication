from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
import datetime

class Auction(models.Model):
    TYPE_CHOICES = [
        ("silent", "Silent"),
        ("live", "Live")
    ]
    published = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.type

class Item(models.Model):
    class Meta:
        abstract = True
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    date = models.DateTimeField(datetime.datetime.now(), default=datetime.datetime.now(), blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SilentItem(Item):
    end = models.DateTimeField(default=None, blank=True, null=True)

class Rule(models.Model):
    title = models.CharField(max_length=200)
    last_modified = models.DateTimeField(default=None, blank=True, null=True)
    rules_content = models.TextField(default=None, blank=True, null=True)
    announcements_content = models.TextField(default=None, blank=True, null=True)
    def __str__(self):
        return self.title

class AuctionUser(AbstractUser):
    auction_number = models.IntegerField(unique=True, default=None, blank=True, null=True)
    has_paid = models.BooleanField(default=False, blank=True, null=True)
    amount = models.FloatField(default=0)

class LiveItem(Item):
    user = models.ForeignKey(AuctionUser, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sold = models.BooleanField(default=False)
    amount = models.FloatField(default=0.00)

class BidSilent(models.Model):
    amount = models.FloatField(default=0)
    item = models.ForeignKey(SilentItem, on_delete=models.CASCADE)
    user = models.ForeignKey(AuctionUser, on_delete=models.CASCADE)
    isWinning = models.BooleanField(default=True)