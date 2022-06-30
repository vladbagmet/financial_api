"""Implements serializers."""

__all__ = ['AccountSerializer', 'BalanceSerializer', 'FundTransferSerializer', 'FundsTransferHistorySerializer']

from rest_framework import serializers
from rest_enumfield import EnumField

from .models import Account, FundsTransferHistory
from .types import CurrencyEnum


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name']


class BalanceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'balance', 'currency']


class FundTransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    currency = EnumField(choices=CurrencyEnum)


class FundsTransferHistorySerializer(serializers.ModelSerializer):
    transaction_id = serializers.UUIDField(source='uuid', read_only=True)
    beneficiary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FundsTransferHistory
        fields = ['transaction_id', 'created_at', 'amount', 'currency', 'beneficiary']

    @staticmethod
    def get_beneficiary(obj: FundsTransferHistory) -> str:
        return obj.beneficiary.name
