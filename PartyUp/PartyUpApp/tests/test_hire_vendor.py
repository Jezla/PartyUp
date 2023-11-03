from django.test import TestCase, RequestFactory
from django.urls import reverse
from PartyUpApp.models import User, Vendor
from PartyUpApp.forms import ChoosePartneredVendorForm
from django.contrib.auth import get_user,authenticate
from PartyUpApp.views import login

"""This class tests the vendor hire
functionality for when the users want to 
hire the servies of a vendor for their events"""
class HireVendorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # test users
        test_user1 = User.objects.create_user(
            username='test1', password='aa11bb22', email="testuser@user.com")
        test_user1.is_member=True
        test_user1.is_vendor=False
        test_user1.save()
    
    def test_hire_loads_properly(self):
        """The hire vendor page loads properly"""
        # test user
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get('/partyup/hire_vendors/')
        self.assertEqual(response.status_code, 200)
    
    def test_hire_url_accessible_by_name(self):
        """The hire vendor url is accessible by name and loads the correct template"""
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get(reverse('partyupapp:choose_vendors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/hire_vendors.html')
    
    def test_hire_unauthenticated(self):
        """Unauthenticated vendor hire"""
        response = self.client.get('/partyup/hire_vendors/')
        self.assertRedirects(response, expected_url=reverse('partyupapp:login'), 
            status_code=302, target_status_code=200)
    
    def test_no_hire_successful(self):
        """Successful no vendor hire (ie the user does not hire a vendor for their event)"""
        login = self.client.login(username='test1', password='aa11bb22')
        data= {"vendor_list":[""]}
        response = self.client.post('/partyup/hire_vendors/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
        session = self.client.session
        vendors = session['vendor_list']
        assert len(vendors)==0
    
    def test_hire_successful_1(self):
        """The user successfully hires one vendor for their event"""
        # test vendor
        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testvendor1@vendor.com")
        test_vendor1 = Vendor(
            user=test_user2, type='MC', address=None)
        test_user2.is_member=False
        test_user2.is_vendor=True
        test_vendor1.vendor_id = test_user2.id
        test_vendor1.save()

        login = self.client.login(username='test1', password='aa11bb22')
        data= {"vendor_list":["test2"]}
        response = self.client.post('/partyup/hire_vendors/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
        session = self.client.session
        vendors = session['vendor_list']
        assert len(vendors)==1
        assert 'test2' in vendors
    
    def test_hire_successful_2(self):
        """The user successfully hires two vendors for their event"""
        # test vendor 1
        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testvendor1@vendor.com")
        test_vendor1 = Vendor(
            user=test_user2, type='MC', address=None)
        test_user2.is_member=False
        test_user2.is_vendor=True
        test_vendor1.vendor_id = test_user2.id
        test_vendor1.save()

        # test vendor 2
        test_user3 = User.objects.create_user(
            username='test3', password='aa11bb22', email="testvendor2@vendor.com")
        test_vendor2 = Vendor(
            user=test_user3, type='DJ', address=None)
        test_user3.is_member=False
        test_user3.is_vendor=True
        test_vendor2.vendor_id = test_user3.id
        test_vendor2.save()

        login = self.client.login(username='test1', password='aa11bb22')
        data= {"vendor_list":["test2,test3"]}
        response = self.client.post('/partyup/hire_vendors/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
        session = self.client.session
        vendors = session['vendor_list']
        assert len(vendors)==2
        assert 'test2' in vendors
        assert 'test3' in vendors

    
    # ======================================================
    # Test ChoosePartneredVendorForm

    def test_invalid_username (self):
        """Tests that the form gives error when invalid vendor user is entered"""
        # test vendor 1
        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testvendor1@vendor.com")
        test_vendor1 = Vendor(
            user=test_user2, type='MC', address=None)
        test_user2.is_member=False
        test_user2.is_vendor=True
        test_vendor1.vendor_id = test_user2.id
        test_vendor1.save()

        data= {"vendor_username": "testinvelid"}
        form = ChoosePartneredVendorForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_vendor_type (self):
        """Tests that the form gives error when invalid vendor type is entered"""
        # test vendor 1
        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testvendor1@vendor.com")
        test_vendor1 = Vendor(
            user=test_user2, type='invalid', address=None)
        test_user2.is_member=False
        test_user2.is_vendor=True
        test_vendor1.vendor_id = test_user2.id
        test_vendor1.save()

        data= {"vendor_username": "test2"}
        form = ChoosePartneredVendorForm(data=data)
        self.assertFalse(form.is_valid())
