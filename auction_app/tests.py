from django.test import TestCase
from django.urls import reverse

from auction_app.models import AuctionUser
from auction_app.views import *
from django.test.utils import setup_test_environment
from auction_app.views import *

class CreateAccountTest(TestCase):
    def setUp(self):
        init_test_db()


class SilentTest(TestCase):
    def setUp(self):
        init_test_db()

    def testPage(self):
        login = self.client.login(username='user1', password='letmepass')
        self.assertTrue(login)
        response = self.client.get(reverse('silent'))
        self.assertIsNotNone(response.context)
        print('#####', type(response.context))

    def setDown(self):
        nukeDB()

class PaymentViewTest(TestCase):
    def setUp(self):
        init_test_db()

    def test_number_of_users(self):
        login = self.client.login(username='admin', password='letmepass')
        response = self.client.get(reverse('payment'))
        self.assertEqual(len(response.context['users']), 3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('payment'))
        self.assertRedirects(response, '/login/?next=/payment')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='letmepass')
        response = self.client.get(reverse('payment'))
        self.assertEqual(str(response.context['user']), 'admin')
        self.assertEqual(response.status_code, 200)

    def test_user_payment_amount(self):
        login = self.client.login(username='admin', password='letmepass')
        response = self.client.get(reverse('payment'))
        # print(response.context['users'])
        for user in response.context['users']:
            if user.username == 'user2':
                self.assertEqual(user.amount, 100)
            elif user.username == 'user1':
                self.assertEqual(user.amount, 120)
            else:
                self.assertEqual(user.amount, 0)

    def test_redirect_if_not_admin(self):
        login = self.client.login(username='user1', password='letmepass')
        response = self.client.get(reverse('users'))
        self.assertRedirects(response, '/home/?next=/users')

class UsersViewTest(TestCase):
    def setUp(self):
        init_test_db()

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='letmepass')
        # print(login)
        response = self.client.get(reverse('users'))
        # print(response)
        self.assertEqual(str(response.context['user']), 'admin')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('users'))
        self.assertRedirects(response, '/login/?next=/users')

    def test_users_returned(self):
        login = self.client.login(username='admin', password='letmepass')
        response = self.client.get(reverse('users'))
        self.assertEqual(len(response.context['users']), 3)

    def test_redirect_if_not_admin(self):
        login = self.client.login(username='user1', password='letmepass')
        response = self.client.get(reverse('users'))
        self.assertRedirects(response, '/home/?next=/users')

    def test_one_plus_one_equals_two(self):
        # print("Method: test_one_plus_one_equals_two.")
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
        new_bid = BidSilent(item=item, amount=12.00, user=AuctionUser.objects.get(auction_number=20))
        new_bid.save()
        # populated the live database too
        itemLive = LiveItem(
            title=randomString(),
            description=randomString(),
            imageName=randomString(),
            auction=silentAuction,
        )
        itemLive.user=AuctionUser.objects.get(auction_number=10)
        itemLive.amount = 10.00
        itemLive.sold = True
        itemLive.save()

def nukeDB():
    Auction.objects.all().delete()
    SilentItem.objects.all().delete()
    LiveItem.objects.all().delete()
    Rule.objects.all().delete()
    AuctionUser.objects.all().delete()
    BidSilent.objects.all().delete()
