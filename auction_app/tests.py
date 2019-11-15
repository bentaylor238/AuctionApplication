from django.test import TestCase
from django.urls import reverse
from auction_app.views import *
from django.test.utils import setup_test_environment
# import django
# django.test.utils.setup_test_environment()

# helper function to set up databse
def init_test_db():
    nukeDB()
    AuctionUser.objects.create_user(
        username="user1",
        password="letmepass",
        email="email@email.com",
        first_name="tommy",
        last_name="thompson",
        auction_number=20,
    )
    AuctionUser.objects.create_user(
        username="user2",
        password="letmepass",
        email="email@email.com",
        first_name="johnny",
        last_name="johnson",
        auction_number=10,
    )
    AuctionUser.objects.create_superuser(
        username="admin",
        email="admin@email.com",
        password="letmepass"
    )
    Rule(title="Rules & Announcements",
            last_modified=timezone.now(),
            rules_content="Insert rules here",
            announcements_content="Insert announcements here"
    ).save()
    silentAuction = Auction(type="silent")
    silentAuction.save()
    liveAuction = Auction(type="live")
    liveAuction.save()
    for i in range(10):
        item = SilentItem(
            title=randomString(), 
            description=randomString(), 
            imageName=randomString(), 
            auction=silentAuction
        )
        item.save()
        user = AuctionUser.objects.all().first()
        user.save()
        # populated the live database too
        itemLive = LiveItem(
            title=randomString(),
            description=randomString(),
            imageName=randomString(),
            auction=silentAuction,
        )
        itemLive.save()

def nukeDB():
    Auction.objects.all().delete()
    SilentItem.objects.all().delete()
    LiveItem.objects.all().delete()
    Rule.objects.all().delete()
    AuctionUser.objects.all().delete()
    # BidSilent.objects.all().delete()
    # BidLive.objects.all().delete()


class SilentTest(TestCase):
    def setUp(self):
        init_test_db()

    def testPage(self):
        login = self.client.login(username='user1', password='letmepass')
        self.assertTrue(login)
        response = self.client.get(reverse('silent'))
        # self.assertIsNotNone(response.context)
        print('#####', type(response.context))

    def setDown(self):
        nukeDB()



class CreateAccountTest(TestCase):
    def setUp(self):
        init_test_db()
