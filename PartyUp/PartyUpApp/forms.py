from ast import Add
from cProfile import label
from datetime import datetime

import email

from importlib.metadata import requires
from pyexpat import model
from tracemalloc import start
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from address.forms import AddressField
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, ModelForm, PasswordInput

from PartyUpApp.models import Event, Item, User, Vendor, Ratings

# A member is a normal user
# A vendor is a business partner
account_type_choices = (
    ("Member", "Member"),
    ("Vendor", "Vendor")
)

# A vendor can be any of the following choices
vendor_type_choices = (
    ("Venue", "Venue"),
    ("DJ", "DJ"),
    ("Decorator", "Decorator"),
    ("MC", "MC")
)

# User registration form
class UserSignUpForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=account_type_choices, required=True)
    vendor_type = forms.ChoiceField(choices=vendor_type_choices, required=False)
    number = PhoneNumberField(region='AU', required=True)
    address = AddressField(required=False)

    class Meta:
        model = User
        fields = ["account_type", "vendor_type", "username", "email", "password1", "password2", "number", "address", "display_name"]
        labels = {"account_type": "Register as: ", "vendor_type": "Vendor Type", "password1": "Password", "password2": "Confirm Password", "number": "Mobile Number", "address": "Address", "display_name": "Display Name"}

# Initial party event creating form
class PartyEventInfoForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)

    class Meta:
        model = Event
        fields = ["name", "description"]
        labels = {"name": "Party Name", "description": "Party Description", "start_date": "Start Time", "end_date": "End Time"}
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date:
            if not (timezone.now() <= start_date):
                self.add_error('start_date', ValidationError(_('Invalid start date.'), code='invalid'))
            if not (timezone.now() <= end_date):
                self.add_error('end_date', ValidationError(_('Invalid end date.'), code='invalid'))
            if not (start_date <= end_date):
                self.add_error(None, ValidationError(_('End date cannot preceed start date.'), code='invalid'))
            diff = end_date - start_date
            hours = diff.total_seconds() / 60 / 60
            if hours < 1:
                self.add_error(None, ValidationError(_('Party Duration must be at least 1 hour'), code='invalid'))

# Form to choose your own venue when creating events 
# (when you don't want to choose a partnered venue)
class ChooseOwnVenueForm(forms.Form):
    address = AddressField(required=False)

    def clean(self):
        cleaned_data = super().clean()

# Form to choose a partnered venue when creating the event
class ChoosePartneredVenueForm(forms.Form):
    venue_username = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['venue_username']
        user = User.objects.filter(username=username)
        if len(user) == 1:
            if user[0].is_vendor:
                venue = Vendor.objects.filter(user_id=user[0].id)
                if len(venue) == 1:
                    if venue[0].type == "Venue":
                        return self.cleaned_data
        self.add_error('venue_username', ValidationError(_(f'Venue with username {username} does not exist.'), code='invalid'))


# Form to choose a partnered vendor when creating a party
class ChoosePartneredVendorForm(forms.Form):
    vendor_username = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['vendor_username']

        vendor = Vendor.objects.filter(user__username=username)
        if vendor.exists():
            if len(vendor) == 1:
                if vendor[0].type in ['DJ', 'Decorator', 'MC']:
                    return self.cleaned_data
        self.add_error('vendor_username', ValidationError(_(f'Vendor with username {username} does not exist.'), code='invalid'))

# Form for inviting guests to the party (note that only registered users can get invited)
class InviteGuestsForm(forms.Form):
    # click add button and username gets transferred into the guest list, save the guest list for future when submitting form
    guest_username = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['guest_username']
        user = User.objects.filter(username=username)
        if len(user) == 1:
            if user[0].is_member:
                return username
            raise forms.ValidationError(u'User with username "%s" does not exist.' % username)
        raise forms.ValidationError(u'User with username "%s" does not exist.' % username)

# Form for creating a party checklist
class EnterChecklistForm(forms.ModelForm):
    # have an empty table on the view with empty cell as the first row, enter name and desc and click add 
    # and then progressively add cells the more the user adds items
    class Meta:
        model = Item
        fields = ["name"]
        labels = {"name": "Name"}

# Form to create a party music playlist
class PartyPlaylistForm(forms.Form):
    playlist_name = forms.CharField(max_length=300)
    playlist_search = forms.CharField(max_length=300)
    track_search = forms.CharField(max_length=300)
    track_id = forms.CharField(max_length=300)

# Form to update user details
class UserUpdateForm(ModelForm):
    class Meta:
        model = User 
        fields = ["display_name","email","phone_number"]
        labels = {"display_name":"Display Name","email":"Email","phone_number":"Phone Number"}

# For updating passwords (inherits django's password change form) 
class UserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User 
        

# For updating vendor details (price, description,rating, type)
class VendorUpdateForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ["address","type","description","price"]
        exclude = ['rating']
        labels = {"type":"Type","address":"Address","price":"Price","description":"Description"}

class VendorRatingForm(ModelForm):
    class Meta:
        model = Ratings
        fields = ["vendor_user", "rating"]