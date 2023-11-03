from django.test import TestCase, RequestFactory
from django.urls import reverse
from PartyUpApp.models import User, Vendor
from PartyUpApp.forms import UserSignUpForm
from django.contrib.auth import get_user,authenticate,get_user_model
from PartyUpApp.views import login


"""This class tests the register functionality 
for different types of users"""
class RegisterTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'aa11bb22'
        self.invalid_pass = 'password'
        self.number = "0410000000"
        self.address = "1 Street, City, Country"
    
    def test_register_loads_properly (self):
        """The regsiter page loads properly"""
        response = self.client.get('/partyup/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_url_accessible_by_name (self):
        """The register url is accessible by name and loads the correct template"""
        response = self.client.get(reverse('partyupapp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/register.html')
    
    def test_successful_rego_1 (self):
        """Successful registration by the member"""
        response = self.client.post('/partyup/register/', data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            "display_name":self.username,
            "account_type": "Member",
            "number": self.number
        })

        self.assertRedirects(response, expected_url=reverse('partyupapp:user_home'), 
            status_code=302, target_status_code=200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
    
    def test_successful_rego_2 (self):
        """Successful registration by the vendor"""
        response = self.client.post('/partyup/register/', data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            "display_name":self.username,
            "account_type": "Vendor",
            "number": self.number,
            "vendor_type": "Venue",
            "address": self.address
        })

        self.assertRedirects(response, expected_url=reverse('partyupapp:vendor_home'), 
            status_code=302, target_status_code=200)
        users = get_user_model().objects.all()
        vendors = Vendor.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(vendors.count(), 1)
    
    def test_unsuccessful_rego_1(self):
        """Unsuccessful registration by the vendor
        password is too weak"""
        response = self.client.post('/partyup/register/', data={
            'username': self.username,
            'email': self.email,
            'password1': "123",
            'password2': "123",
            "display_name":self.username,
            "account_type": "Vendor",
            "number": self.number,
            "vendor_type": "Venue",
            "address": self.address
        })

        # user doesn't get redirected
        self.assertEqual(response.status_code, 200)
        # new user isn't added
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_unsuccessful_rego_2(self):
        """Unsuccessful registration because passwords do not match"""
        response = self.client.post('/partyup/register/', data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': "unmatchingpassword",
            "display_name":self.username,
            "account_type": "Vendor",
            "number": self.number,
            "vendor_type": "Venue",
            "address": self.address
        })

        # user doesn't get redirected
        self.assertEqual(response.status_code, 200)
        # new user isn't added
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)
    
    # ===========================================================
    # testing the registration form
    def test_signup_form_1(self):
        """Tests the login form individually"""
        """missign username"""
        data={
            'username': "",
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            "display_name":self.username,
            "account_type": "Vendor",
            "number": self.number,
            "vendor_type": "Venue",
            "address": self.address
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_2(self):
        """Tests the login form individually"""
        """missign email"""
        data={
            'username': self.username,
            'email': "",
            'password1': self.password,
            'password2': self.password,
            "display_name":self.username,
            "account_type": "Vendor",
            "number": self.number,
            "vendor_type": "Venue",
            "address": self.address
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_3(self):
        """Tests the login form individually"""
        """missign password"""
        data={
            'username': self.username,
            'email':self.password,
            'password1': "",
            'password2': "",
            "display_name":self.username,
            "account_type": "Member",
            "number": self.number
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_4(self):
        """Tests the login form individually"""
        """unmatching passwords"""
        data={
            'username': self.username,
            'email':self.password,
            'password1': self.password,
            'password2': "unmatchingpass123",
            "display_name":self.username,
            "account_type": "Member",
            "number": self.number
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_5(self):
        """Tests the login form individually"""
        """invalid number"""
        data={
            'username': self.username,
            'email':self.password,
            'password1': self.password,
            'password2': self.password,
            "display_name":self.username,
            "account_type": "Member",
            "number": "09100000000"
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())
