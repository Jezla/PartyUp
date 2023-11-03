from enum import unique
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.db.models import Q,F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.functions import Now
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


# user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    phone_number = PhoneNumberField(region='AU', max_length=12)
    REQUIRED_FIELDS = ['email', 'display_name'] 
    # REQUIRED_FIELDS are not the required fields in forms, but the required fields when creating a user
    # via the command line using createsuperuser command

# vendors
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(max_length=160, null=True, blank=True)
    address = AddressField(null=True, blank=True) # Only Vendors of Type Venue should have an address, null=True means that when deleting an AddressField from Vendor, it turns into null, rather than deleting the Vendor themselves
    type = models.CharField(max_length=50)
    price = models.FloatField(null=True) ##add constraint to disallow negative amounts



# party event
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=160)
    playlist_id = models.CharField(max_length=100,null=True)
    address = AddressField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Party checklist item
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=160, null=True)
    acquired = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

# Event Guests model
class Guest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

# Payment transaction model
# (for when the users pay the vendors)
class Transaction(models.Model):
    amount = models.FloatField() ##add constraint to disallow negative amounts
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    # Amount paid cannot be <0
    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(amount__gte=0), name= "amount non negative")
        ]
    
    def clean(self):
        if self.amount<0:
            raise ValidationError({'amount':_('amount needs to be non negative.')})

# bookings (between a user and a vendor whose been hired by them)
class Booking(models.Model):
    start_date = models.DateTimeField() ##add constraint and form validation error on past dates 
    end_date = models.DateTimeField() ##add constraint and form validation error on past dates and start_date-end_date >= 15min???
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100, blank=True)

    class Meta:
        # end_date > start_date and start_date >= now
        constraints = [
            models.CheckConstraint(check=Q(start_date__lte=F('end_date'),start_date__gte=Now()), name= "correct date_time")
        ]
    
    def clean(self):
        if not (timezone.now() <= self.start_date <= self.end_date):
            raise ValidationError('Invalid start and end datetime')

# This is for using spotify API to create playlists for a party
# You need spotify authentication for this
class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    refresh_token = models.CharField(max_length=2000)
    access_token = models.CharField(max_length=2000)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Ratings(models.Model):
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor_user = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True) ##add constraint and form validation error to check for ranges

    class Meta:
        constraints = [
            models.CheckConstraint(check=(Q(rating__gte=1, rating__lte=5) | Q(rating__isnull=True)), name="rating1-5"),
        ]

    def clean(self):
        if self.rating != None:
            if self.rating > 5 or self.rating < 1:
                raise ValidationError({'rating': _('rating needs to be between 1 and 5 inclusive.')})
