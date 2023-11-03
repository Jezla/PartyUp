from django.test import TestCase
from django.contrib.auth import get_user_model
from PartyUpApp.models import User, Vendor, Event, Item, Guest, Transaction, Booking, SpotifyToken, Ratings
import datetime
from django.utils import timezone

"""This class unit tests the models in our webiste to ensure
they are being intialised correctly
"""
class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='123123@gmail.com', display_name="test")
        Event.objects.create(name="my party", description="birthday", playlist_id='1', user=user)
        Vendor.objects.create(user=user, description="vendor text", type="food")

    def test_user(self):
        user = User.objects.get(email='123123@gmail.com')
        name_label = user.display_name
        email_label = user.email
        self.assertEquals(name_label, 'test')
        self.assertEquals(email_label, '123123@gmail.com')
        self.assertFalse(user.is_member)
        self.assertFalse(user.is_vendor)

    def test_vendor(self):
        # user = User.objects.get(id=1)
        vendor = Vendor.objects.get(description="vendor text")
        description_label = vendor.description
        type_label = vendor.type
        self.assertEquals(description_label, 'vendor text')
        self.assertEquals(type_label,'food')

    def test_event(self):
        # user = User.objects.get(id=1)
        event = Event.objects.get(name="my party")
        description_label = event.description
        playlist_label = event.playlist_id
        self.assertEquals(description_label, 'birthday')
        self.assertEquals(playlist_label, '1')

    def test_item(self):
        event = Event.objects.get(name="my party")
        item = Item.objects.create(name="boot", description="leather", event=event)
        name_label = item.name
        description_label = item.description
        event_name = item.event.name
        self.assertEquals(name_label, 'boot')
        self.assertEquals(description_label, 'leather')
        self.assertEquals(event_name, 'my party')
        self.assertFalse(item.acquired)

    def test_guest(self):
        user = User.objects.get(email='123123@gmail.com')
        event = Event.objects.get(name="my party")
        guest = Guest.objects.create(user=user, event=event)
        event_name = guest.event.name
        user_name = guest.user.display_name
        self.assertEquals(event_name, 'my party')
        self.assertEquals(user_name, 'test')

    def test_transaction(self):
        user = User.objects.get(email='123123@gmail.com')
        event = Event.objects.get(name="my party")
        transaction = Transaction.objects.create(amount=100.0, user=user, event=event)
        amount_cost = transaction.amount
        user_name = transaction.user.display_name
        event_name = transaction.event.name
        self.assertEquals(amount_cost, 100.0)
        self.assertEquals(user_name, 'test')
        self.assertEquals(event_name, 'my party')

    def test_booking(self):
        datetime.datetime.now(tz=timezone.utc)
        start = datetime.datetime(2023, 5, 17, 12, 12, 12, tzinfo=timezone.utc)
        end = datetime.datetime(2023, 6, 17, 12, 12, 12, tzinfo=timezone.utc)
        user = User.objects.get(email='123123@gmail.com')
        event = Event.objects.get(name="my party")
        vendor = Vendor.objects.get(description="vendor text")
        booking = Booking.objects.create(start_date=start,end_date=end, vendor=vendor, user=user, event=event, vendor_name="butler")
        user_name = booking.user.display_name
        event_name = booking.event.name
        vendor_desc = booking.vendor.description
        self.assertEquals(user_name, 'test')
        self.assertEquals(event_name, 'my party')
        self.assertEquals(vendor_desc, 'vendor text')

    def test_spotify(self):
        user = User.objects.get(email='123123@gmail.com')
        datetime.datetime.now(tz=timezone.utc)
        expiry = datetime.datetime(2024, 6, 17, 12, 12, 12, tzinfo=timezone.utc)
        spotify_token = SpotifyToken.objects.create(user=user, refresh_token="reftoken", expires_in=expiry, access_token="acctoken")
        user_name = spotify_token.user.display_name
        refresh_token = spotify_token.refresh_token
        access_token = spotify_token.access_token
        self.assertEquals(user_name, 'test')
        self.assertEquals(refresh_token, 'reftoken')
        self.assertEquals(access_token, 'acctoken')

    def test_ratings(self):
        user = User.objects.get(email='123123@gmail.com')
        vendor = Vendor.objects.get(description="vendor text")
        rating = Ratings.objects.create(rating_user=user, vendor_user=vendor, rating=5)
        user_name = rating.rating_user.display_name
        vendor_desc = rating.vendor_user.description
        given_rating = rating.rating
        self.assertEquals(user_name, 'test')
        self.assertEquals(vendor_desc, 'vendor text')
        self.assertEquals(5, given_rating)