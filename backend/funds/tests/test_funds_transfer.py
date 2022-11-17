from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from funds.models import Account
from funds.types import CurrencyEnum


class FundsTransferTest(APITestCase):
    """Funds transfers tests."""

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

    def test_successful_funds_transfer(self):
        """Testing successful funds transfer."""

        # If Django's default User model will be replaced at some point, this should keep tests up-to-date
        user_model = get_user_model()

        amount_to_transfer = 100
        # Since API does not have a functionality to add funds to the account, using direct objects manipulation here
        account_with_funds = Account.objects.create(
            owner=user_model.objects.get(username=self.username),
            name='Account With Funds',
            balance=amount_to_transfer
        )
        account_without_funds = Account.objects.create(
            owner=user_model.objects.get(username=self.username),
            name='Account Without Funds'
        )

        funds_transfer_api_url = reverse(
            'transfer_funds', kwargs={
                'sender_account_id': account_with_funds.uuid,
                'beneficiary_account_id': account_without_funds.uuid
            }
        )

        self.assertEqual(account_without_funds.balance, 0)
        funds_transfer_response = self.client.post(
            funds_transfer_api_url,
            {'amount': amount_to_transfer, 'currency': CurrencyEnum.USD},
            HTTP_AUTHORIZATION=self.auth_string
        )
        account_without_funds.refresh_from_db()
        self.assertEqual(funds_transfer_response.status_code, status.HTTP_200_OK)
        self.assertEqual(funds_transfer_response.data['message'], 'Funds are transferred successfully')
        self.assertIn(
            member='transaction_id',
            container=funds_transfer_response.data,
            msg='Successful funds transfer should include `transaction_id` key in the response'
        )
        self.assertEqual(account_without_funds.balance, amount_to_transfer)

    def test_insufficient_funds_exception(self):
        """Testing funds transfer when sender does not have enough funds to make a transfer."""
        user_model = get_user_model()
        amount_to_deposit = 100
        amount_to_transfer = amount_to_deposit + 1

        account_with_funds = Account.objects.create(
            owner=user_model.objects.get(username=self.username),
            name='Account With Funds',
            balance=amount_to_deposit
        )
        account_without_funds = Account.objects.create(
            owner=user_model.objects.get(username=self.username),
            name='Account Without Funds'
        )

        funds_transfer_api_url = reverse(
            'transfer_funds', kwargs={
                'sender_account_id': account_with_funds.uuid,
                'beneficiary_account_id': account_without_funds.uuid
            }
        )
        funds_transfer_response = self.client.post(
            funds_transfer_api_url,
            {'amount': amount_to_transfer, 'currency': CurrencyEnum.USD},
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(funds_transfer_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(funds_transfer_response.data[settings.API_ERROR_KEY][0], 'Insufficient funds balance')
