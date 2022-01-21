from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from funds.models import Account
from funds.types import CurrencyEnum


class FundsTransferHistoryTest(APITestCase):
    """Funds transfers operations history tests."""

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

    def test_successful_transfers_history_retrieval(self):
        """Testing successful funds transfer history retrieval."""

        user_making_a_request = get_user_model().objects.get(username=self.username)
        amount_to_transfer = 100

        account_with_funds = Account.objects.create(
            owner=user_making_a_request,
            name='Account With Funds',
            balance=amount_to_transfer
        )
        account_without_funds = Account.objects.create(
            owner=user_making_a_request,
            name='Account Without Funds'
        )
        funds_history_api_url = reverse(
            'retrieve_funds_transfers_history', kwargs={
                'account_id': account_with_funds.uuid
            }
        )
        no_history_response = self.client.get(
            funds_history_api_url,
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(no_history_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            no_history_response.data,
            [],
            msg='Before any funds transfers history for the newly-created account should by empty'
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
        self.assertEqual(funds_transfer_response.status_code, status.HTTP_200_OK)

        response_with_transfers_history = self.client.get(
            funds_history_api_url,
            HTTP_AUTHORIZATION=self.auth_string
        )
        self.assertEqual(response_with_transfers_history.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response_with_transfers_history.data),
            1,
            msg='After 1 successful funds transfer there should be 1 transfer history record'
        )
        self.assertEqual(
            str(funds_transfer_response.data['transaction_id']),
            str(response_with_transfers_history.data[0]['transaction_id']),
            msg='Transaction ids for transfer and transfer history record should match'
        )
