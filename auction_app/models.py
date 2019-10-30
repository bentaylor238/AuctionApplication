from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
import datetime

class Auction(models.Model):
    published = models.BooleanField(default=False)
    type = models.CharField( max_length=50)

class Item(models.Model):
    class Meta:
        abstract = True
    title = models.CharField(max_length=200, default='')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    date = models.DateTimeField(datetime.datetime.now(), default=datetime.datetime.now())
    imageName = models.CharField(max_length=50, default='')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True, blank=True)

class SilentItem(Item):
    start = models.DateTimeField(default=None, blank=True, null=True)
    end = models.DateTimeField(default=None, blank=True, null=True)

class LiveItem(Item):
    orderInQueue = models.IntegerField()

class Rules(models.Model):
    title = models.CharField(max_length=200)
    lastModified = models.DateTimeField()
    rulesContent = models.TextField()
    announcementsContent = models.TextField()
    def __str__(self):
        return self.title

class User(AbstractUser):
    name = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=200, default='')


# class User(models.Model):
#     name = models.CharField(max_length=200, default='')
#     username = models.CharField(max_length=200, default='')
#     auction_number = models.IntegerField(default=None, blank=True, null=True)
#     email = models.EmailField(max_length=200, default='')
#     password = models.CharField(max_length=200, default='')
#     is_admin = models.BooleanField(default=False)
#     # silentItem = models.ForeignKey(SilentItem, on_delete=models.CASCADE)

class Bid(models.Model):
    amount = models.FloatField(default=0)
    item = models.ForeignKey(SilentItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class SilentAuction(models.Model):
#     published = models.BooleanField(default=False)

# class LiveAuction(models.Model):
#     published = models.BooleanField(default=False)

