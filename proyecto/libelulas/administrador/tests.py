from django.test import TestCase
from .models import User
from django.db.models import QuerySet

# Create your tests here.

'''
class AdminTests(TestCase):
    def setUp(self):
        User.objects.create(
            firstname= 'testname',
            username='testuser',
            email='test-email',
            password='12345',
            confirm_password='12345'
        )


    def test_Admin_create(self):
        User.objects.create(
            firstname='Paco',
            username='paco123',
            email='paco123@paco.com',
            password='12345',
            confirm_password='12345'
        )
    def test_Admin_read(self):
        admin_all = User.objects.all()
        self.assertIsInstance(admin_all, QuerySet)
'''