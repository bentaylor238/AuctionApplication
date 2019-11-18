from django.test import TestCase, Client
from django.urls import reverse
from auction_app.forms import *
from django.utils import timezone
from auction_app.models import AuctionUser
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

class LiveAuction(TestCase):
   # helper methods
    def setUp(self):
        init_test_db()

    def publishAuction(self):
        liveAuction = Auction.objects.get(type='live')
        liveAuction.published = True
        liveAuction.save()

    # test cases
    def test_page(self):
        self.assertTrue(self.client.login(username='admin', password='letmepass'))
        response = self.client.get(reverse('live'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('live.html')

    def test_Non_published_context(self):
        self.assertTrue(self.client.login(username='admin', password='letmepass'))
        response = self.client.get(reverse('live'))
        self.assertEqual(response.context['published'], False)
        self.assertEqual(len(response.context['items']), 10)
        self.assertEqual(response.context['currentItem'].title, LiveItem.objects.filter(sold=False).order_by('pk').first().title)

    def test_published_context(self):
        self.publishAuction()
        self.assertTrue(self.client.login(username='admin', password='letmepass'))
        response = self.client.get(reverse('live'))
        self.assertEqual(response.context['published'], True)
        self.assertEqual(len(response.context['items']), 9)
        self.assertEqual(response.context['currentItem'].title, LiveItem.objects.filter(sold=False).order_by('pk').first().title)

    def test_placeBid(self):
        self.publishAuction()
        self.assertTrue(self.client.login(username='admin', password='letmepass'))
        response = self.client.get(reverse('live'))
        keyOfFirstCurrentItem = response.context['currentItem'].pk
        c = Client()
        postAttempt = c.post(reverse('sellLiveItem'), {'auction_number': 20, 'pk': keyOfFirstCurrentItem, 'amount': 30})
        self.assertEqual(postAttempt.status_code, 302)
        response = self.client.get(reverse('live'))
        self.assertNotEqual(keyOfFirstCurrentItem, response.context['currentItem'].pk)


class CreateAccountTest(TestCase):
    def setUp(self):
        init_test_db()

    def test_login_redirect(self):
        response = self.client.get(reverse('create_item'))
        self.assertRedirects(response, '/login/?next=/create_item')

    def test_login(self):
        print(AuctionUser.objects.get(username="user1"))
        loggedIn = self.client.login(username="admin", password="letmepass")
        print(loggedIn)

# helper function to set up database
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
            auction=silentAuction
        )
        item.save()
        user = AuctionUser.objects.all().first()
        user.save()
        new_bid = BidSilent(item=item, amount=12.00, user=AuctionUser.objects.get(auction_number=20))
        new_bid.save()
        itemLive = LiveItem(
            title=randomString(),
            description=randomString(),
            auction=silentAuction,
            sold=False
        )
        itemLive.user=AuctionUser.objects.get(auction_number=10)
        itemLive.amount = 10.00
        itemLive.save()

def nukeDB():
    Auction.objects.all().delete()
    SilentItem.objects.all().delete()
    LiveItem.objects.all().delete()
    Rule.objects.all().delete()
    AuctionUser.objects.all().delete()
    BidSilent.objects.all().delete()
    # BidLive.objects.all().delete()



