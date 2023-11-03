from django.test import TestCase, RequestFactory
from django.urls import reverse
from PartyUpApp.models import User, Vendor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user,authenticate
from PartyUpApp.views import login


"""This class tests the login functionality 
for different types of users"""
class LoginTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        # test users
        test_user1 = User.objects.create_user(
            username='test1', password='aa11bb22', email="testuser@user.com")
        test_user1.is_member=True
        test_user1.is_vendor=False
        test_user1.save()

        # test vendor (without address)
        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testvendor1@vendor.com")
        test_vendor1 = Vendor(
            user=test_user2, type='MC', address=None)
        test_user2.is_member=False
        test_user2.is_vendor=True
        test_vendor1.save()

        # test vendor (with address)
        test_user3 = User.objects.create_user(
            username='test3', password='aa11bb22', email="testvendor2@vendor.com")
        test_vendor2 = Vendor(
            user=test_user3, type='Venue', address="1 Stree, City, Country")
        test_user3.is_member=False
        test_user3.is_vendor=True
        test_vendor2.save()

        # test admin
        test_admin= User.objects.create_superuser(
            username='testadmin', password='aa11bb22', email="testadmin@admin.com")
        test_admin.save()
        
    def test_login_loads_properly(self):
        """The index and login page loads properly"""
        response = self.client.get('/partyup/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/partyup/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_url_accessible_by_name(self):
        """The login url is accessible by name and loads the correct template"""
        response = self.client.get(reverse('partyupapp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/login.html')
    
    def test_successful_login(self):
        """The user can log in successfully when providing the
        correct username and password"""
        data = {"username":"test1","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertRedirects(response, expected_url=reverse('partyupapp:user_home'), 
            status_code=302, target_status_code=200)
    
    def test_successful_login_member(self):
        """The user can log in successfully when providing the
        correct username and password"""
        data = {"username":"test1","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertRedirects(response, expected_url=reverse('partyupapp:user_home'), 
            status_code=302, target_status_code=200)
    
    def test_successful_login_vendor_noaddress(self):
        """The vendor can log in successfully when providing the
        correct username and password"""
        data = {"username":"test2","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertRedirects(response, expected_url=reverse('partyupapp:vendor_home'), 
            status_code=302, target_status_code=200)
    
    def test_successful_login_vendor_address(self):
        """The vendor can log in successfully when providing the
        correct username and password"""
        data = {"username":"test3","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertRedirects(response, expected_url=reverse('partyupapp:vendor_home'), 
            status_code=302, target_status_code=200)
    
    def test_unsuccessful_login_1(self):
        """The user provides invalid credentials"""
        data = {"username":"invalid","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/login.html')
    
    def test_unsuccessful_login_2(self):
        """The user provides invalid credentials"""
        data = {"username":"test1","password": "invalid"}
        response = self.client.post('/partyup/login/',data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/login.html')
    
    def test_successful_login_admin(self):
        """The vendor can log in successfully when providing the
        correct username and password"""
        data = {"username":"testadmin","password": "aa11bb22"}
        response = self.client.post('/partyup/login/',data)
        self.assertRedirects(response, expected_url='http://127.0.0.1:8000/admin', 
            status_code=302, target_status_code=200,fetch_redirect_response=False)
            
    # ===========================================================
    # testing the authentication form
    def test_login_form_1(self):
        """Tests the login form individually"""
        userdata = {"username":"nonexisting","password": "aa11bb22"}
        form = AuthenticationForm(data=userdata)
        self.assertFalse(form.is_valid())
    
    def test_login_form_2(self):
        """Tests the login form individually"""
        userdata = {"username":"test1","password": "invalid"}
        form = AuthenticationForm(data=userdata)
        self.assertFalse(form.is_valid())
    
    def test_login_form_3(self):
        """Tests the login form individually"""
        userdata = {"username":"","password": ""}
        form = AuthenticationForm(data=userdata)
        self.assertFalse(form.is_valid())
    
    def test_login_form_4(self):
        """Tests the login form individually"""
        userdata = {"username":"","password": None}
        form = AuthenticationForm(data=userdata)
        self.assertFalse(form.is_valid())