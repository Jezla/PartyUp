from django.test import TestCase, RequestFactory
from django.urls import reverse
from PartyUpApp.models import User, Vendor
from PartyUpApp.forms import InviteGuestsForm
from django.contrib.auth import get_user,authenticate
from PartyUpApp.views import login

"""This class tests the functionality of inviting guests an event"""
class InviteGuestTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        test_user1 = User.objects.create_user(
            username='test1', password='aa11bb22', email="testuser@user.com")
        test_user1.is_member=True
        test_user1.is_vendor=False
        test_user1.save()

        test_user2 = User.objects.create_user(
            username='test2', password='aa11bb22', email="testuser2@user.com")
        test_user2.is_member=True
        test_user2.is_vendor=False
        test_user2.save()

        test_user3 = User.objects.create_user(
            username='test3', password='aa11bb22', email="testuser3@user.com")
        test_user3.is_member=True
        test_user3.is_vendor=False
        test_user3.save()
    
    def test_choose_venue_loads_properly(self):
        """The invite guests page loads properly"""
        # test user
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get('/partyup/invite_guests/')
        self.assertEqual(response.status_code, 200)
    
    def test_venue_url_accessible_by_name(self):
        """The invite guests url is accessible by name and loads the correct template"""
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get(reverse('partyupapp:invite_guests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/invite_guest.html')
    
    def test_choose_venue_unauthenticated(self):
        """Unauthenticated guest invite"""
        response = self.client.get('/partyup/invite_guests/')
        self.assertRedirects(response, expected_url=reverse('partyupapp:login'), 
            status_code=302, target_status_code=200)
    
    def test_invite_no_one(self):
        """user invites no one to the event"""
        login = self.client.login(username='test1', password='aa11bb22')
        data = {"guest_list":['']}
        response = self.client.post('/partyup/invite_guests/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
        session = self.client.session
        guests = session['guest_list']
        assert len(guests)==0

    def test_invite_invalid(self):
        """user invites invalid username"""
        login = self.client.login(username='test1', password='aa11bb22')
        data = {"guest_list":['invlidname']}
        response = self.client.post('/partyup/invite_guests/',data)
        self.assertEqual(response.status_code, 500)
    
    def test_invite_complex(self):
        """user invites valid and invalid usernames"""
        login = self.client.login(username='test1', password='aa11bb22')
        # valid guests
        data = {"guest_list":['test2,test3']}
        response = self.client.post('/partyup/invite_guests/',data)
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        guests = session['guest_list']
        assert len(guests)==2
        assert 'test2' in guests
        assert 'test3' in guests

        # invlid guest
        data = {"guest_list":['invlidname']}
        response = self.client.post('/partyup/invite_guests/',data)
        self.assertEqual(response.status_code, 500)
        

    # ======================================================
    # Test InviteGuestsForm

    def test_invalid_username (self):
        """Tests that the form gives error when invalid guest username is entered
        Tests that the form gives error when vendor username is entered"""

        # test vendor 1
        test_user4 = User.objects.create_user(
            username='test4', password='aa11bb22', email="testvendor4@vendor.com")
        test_vendor1 = Vendor(
            user=test_user4, type='MC', address=None)
        test_user4.is_member=False
        test_user4.is_vendor=True
        test_vendor1.vendor_id = test_user4.id
        test_vendor1.save()

        data= {"guest_username": "test4"}
        form = InviteGuestsForm(data=data)
        self.assertFalse(form.is_valid())