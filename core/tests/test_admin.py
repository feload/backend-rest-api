from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# reverse helps us generate urls.
from django.urls import reverse

class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            'admin@admin.com',
            'Password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@user.com',
            password='Userpass123',
            name='Test user name'
        )


    def test_users_listed(self):
        '''Test that users are listed on user page'''
        # Create an url based from a key (documented in django documetation)
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_user_change_page(self):
        '''Test that the user edit page works'''
        # /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


    def test_create_user_page(self):
        '''Test that the create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)