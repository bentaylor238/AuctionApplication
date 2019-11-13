from django.test import TestCase
from django.urls import reverse

# from auction_app.models import *
# from .forms import *

class CreateAccountTest(TestCase):
    def setUp(self):
        init_test_db()

# Create your tests here.
class UsersViewTest(TestCase):
    @classmethod
    def setup(self):
        init_test_db()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('users'))
        self.assertRedirects(response, '/login/?next=/users')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='letmepass')
        print(login)
        response = self.client.get(reverse('users'))
        print(response)
        self.assertEqual(str(response.context['user']), 'admin')
        self.assertEqual(response.status_code, 200)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

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
            orderInQueue=i
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
