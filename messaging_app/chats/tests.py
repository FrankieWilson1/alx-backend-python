from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import User


class UserAPITests(APITestCase):
    """
    Test suite for the User API endpoints.
    """
    def setUp(self):
        # Create a user to use for authentication
        self.user = User.objects.create_user(
            username='testuser0',
            email='testuser0@example.com',
            password='Testpassword0'
        )
        self.client.force_authenticate(user=self.user)
        
        def test_list_users(self):
        """
        Ensuere list of users can be retrieved.
        """
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
