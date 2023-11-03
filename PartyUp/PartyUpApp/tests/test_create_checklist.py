from django.test import TestCase, RequestFactory
from django.urls import reverse
from PartyUpApp.models import User, Vendor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user,authenticate
from PartyUpApp.views import login

"""This class tests the functionality of creating an event checklist"""
class CreateCheckTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        test_user1 = User.objects.create_user(
            username='test1', password='aa11bb22', email="testuser@user.com")
        test_user1.is_member=True
        test_user1.is_vendor=False
        test_user1.save()

    def test_checklist_loads_properly(self):
        """The create checklist page loads properly"""
        # test user
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get('/partyup/checklist/')
        self.assertEqual(response.status_code, 200)
    
    def test_checklist_url_accessible_by_name(self):
        """The checklist url is accessible by name and loads the correct template"""
        login = self.client.login(username='test1', password='aa11bb22')
        response = self.client.get(reverse('partyupapp:checklist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PartyUpApp/checklist.html')
    
    def test_checklist_unauthenticated(self):
        """Unauthenticated checklist creation"""
        response = self.client.get('/partyup/checklist/')
        self.assertRedirects(response, expected_url=reverse('partyupapp:login'), 
            status_code=302, target_status_code=200)
    
    def test_checklist_successful_empty_list(self):
        """Successful checklist creation 1"""
        login = self.client.login(username='test1', password='aa11bb22')
        data= {"item_list":['']}
        response = self.client.post('/partyup/checklist/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
    
    def test_checklist_successful_nonempty_list_1(self):
        """Successful checklist creation 2"""
        login = self.client.login(username='test1', password='aa11bb22')
        data= {"item_list":["meat,coke"]}
        response = self.client.post('/partyup/checklist/',data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Success'}
        )
        session = self.client.session
        items = session['item_list']
        assert len(items)==2
        assert 'meat' in items
        assert 'coke' in items
    
"""checklist page uses a simple form called EnterChecklist with 
only one field: item. Therefore, testing it is trivial and almost
impossible."""