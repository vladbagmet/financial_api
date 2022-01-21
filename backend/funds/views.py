import contextlib
import logging

from rest_framework import generics, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Account, FundsTransferHistory
from .serializers import AccountSerializer, BalanceSerializer, FundTransferSerializer, FundsTransferHistorySerializer
from .exceptions import AccountNotExist, InvalidAccountId, SameNameAccountExists, FundsTransferException
from .logic.funds_transfer.internal_system import InternalSystemFundsTransfer, AbstractFundsTransfer


class AccountView(generics.GenericAPIView):
    serializer_class = AccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with contextlib.suppress(IntegrityError):
            account: Account = Account.objects.create(owner=request.user, **serializer.validated_data)
            return Response(self.serializer_class(account).data, status.HTTP_201_CREATED)
        raise SameNameAccountExists(
            {settings.API_ERROR_KEY: [
                f'Account with name `{serializer.validated_data["name"]}` '
                f'already exists for user `{request.user.username}`'
            ]}
        )


class BalanceView(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    queryset = Account.objects.all()

    def get(self, request, account_id, *args, **kwargs):
        try:
            queryset = self.queryset.get(owner=request.user, uuid=account_id)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        except ValidationError:
            raise InvalidAccountId({settings.API_ERROR_KEY: [f'Invalid account `{account_id}`']})
        except ObjectDoesNotExist:
            raise AccountNotExist({settings.API_ERROR_KEY: [f'Account `{account_id}` not exist']})


class FundsTransferView(generics.GenericAPIView):
    serializer_class = FundTransferSerializer

    def post(self, request, sender_account_id, beneficiary_account_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sender_account = Account.objects.get(uuid=sender_account_id)
            beneficiary_account = Account.objects.get(uuid=beneficiary_account_id)
        except ValidationError:
            raise InvalidAccountId({settings.API_ERROR_KEY: ['Invalid sender or beneficiary accounts']})
        except ObjectDoesNotExist:
            raise AccountNotExist({settings.API_ERROR_KEY: ['Either sender or beneficiary accounts not exist']})

        try:
            transaction_id: AbstractFundsTransfer = InternalSystemFundsTransfer().make_transfer(
                sender_account=sender_account,
                beneficiary_account=beneficiary_account,
                **serializer.validated_data
            )
        except FundsTransferException as e:
            logging.warning(e)
            raise FundsTransferException({settings.API_ERROR_KEY: e.args})
        return Response(
            {
                'message': 'Funds are transferred successfully',
                'transaction_id': transaction_id
            }
        )


class TransactionsHistoryView(generics.GenericAPIView):
    queryset = FundsTransferHistory.objects.all()
    serializer_class = FundsTransferHistorySerializer

    def get(self, request, account_id, *args, **kwargs):
        try:
            queryset = self.queryset.filter(sender__owner=request.user, sender=account_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError:
            raise InvalidAccountId({settings.API_ERROR_KEY: [f'Invalid account `{account_id}`']})
