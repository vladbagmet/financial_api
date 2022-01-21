from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class AccountOperationTest(APITestCase):
    """Basic account operations tests."""

    @classmethod
    def setUp(cls):
        username = 'test-user'
        password = 'test-password'

        cls.username = username
        cls.client = APIClient()
        cls.account_api_url: str = reverse('create_account')
        cls.user_registration_api_url: str = reverse('register_user')
        cls.token_retrieval_api_url: str = reverse('retrieve_tokens_pairs')

        _ = cls.client.post(cls.user_registration_api_url, {'username': username, 'password': password})
        token_retrieval_response = cls.client.post(
            cls.token_retrieval_api_url,
            {'username': username, 'password': password}
        )
        access_token = token_retrieval_response.data['access']
        cls.auth_string = f'Bearer {access_token}'

    def test_account_creation_no_auth(self):
        """Testing account creation on behalf of not authenticated user fails."""
        response = self.client.post(self.account_api_url, {'name': 'Account 1'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_creation_correct_data(self):
        """Testing account creation for authenticated user with correct inputs."""
        account_name = 'Test Account'
        response = self.client.post(
            self.account_api_url,
            {'name': account_name},
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], account_name)

    def test_same_name_account_creation(self):
        """Testing account creation with the same name and user returns an error."""
        account_name = 'Test Account'
        successful_response = self.client.post(
            self.account_api_url,
            {'name': account_name},
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(successful_response.status_code, status.HTTP_201_CREATED)

        error_response = self.client.post(
            self.account_api_url,
            {'name': account_name},
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(error_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member=settings.API_ERROR_KEY,
            container=error_response.data,
            msg=f'Error response should contain `{settings.API_ERROR_KEY}` key'
        )

    def test_balance_retrieval(self):
        """Testing account balance retrieval."""
        account_name = 'Test Account'
        account_creation_response = self.client.post(
            self.account_api_url,
            {'name': account_name},
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(account_creation_response.status_code, status.HTTP_201_CREATED)

        account_id = account_creation_response.data['id']
        balance_retrieval_api_url = reverse('retrieve_account_balance', kwargs={'account_id': account_id})
        balance_retrieval_response = self.client.get(
            balance_retrieval_api_url,
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(balance_retrieval_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            balance_retrieval_response.data['balance'],
            0,
            'For newly-created accounts balance should be 0'
        )
        self.assertEqual(
            balance_retrieval_response.data['currency'],
            'USD',
            'For newly-created accounts currency should be `USD` if anything else was not specified during creation'
        )
