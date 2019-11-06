from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
import datetime

class Auction(models.Model):
    published = models.BooleanField(default=False)
    type = models.CharField(max_length=50)

class Item(models.Model):
    class Meta:
        abstract = True
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    date = models.DateTimeField(datetime.datetime.now(), default=datetime.datetime.now())
    imageName = models.CharField(max_length=50, default='')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

class SilentItem(Item):
    start = models.DateTimeField(default=None, blank=True, null=True)
    end = models.DateTimeField(default=None, blank=True, null=True)

class LiveItem(Item):
    sold=models.BooleanField(default=False)
    orderInQueue = models.IntegerField()

class Rule(models.Model):
    title = models.CharField(max_length=200)
    last_modified = models.DateTimeField(default=None, blank=True, null=True)
    rules_content = models.TextField(default=None, blank=True, null=True)
    announcements_content = models.TextField(default=None, blank=True, null=True)
    def __str__(self):
        return self.title

class AuctionUser(AbstractUser):
    auction_number = models.IntegerField(default=None, blank=True, null=True)

class Bid(models.Model):
    amount = models.FloatField(default=0)
    item = models.ForeignKey(SilentItem, on_delete=models.CASCADE)
    user = models.ForeignKey(AuctionUser, on_delete=models.CASCADE)

# class SilentAuction(models.Model):
#     published = models.BooleanField(default=False)

# class LiveAuction(models.Model):
#     published = models.BooleanField(default=False)
