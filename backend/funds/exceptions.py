"""Contains app-level custom exceptions."""

__all__ = [
    'AccountNotExist',
    'InvalidAccountId',
    'SameNameAccountExists',
    'FundsTransferException',
    'InsufficientFunds',
    'CurrencyTransferNotSupported',
    'SameAccountTransfersProhibited',
    'IncorrectTransferAmount'
]

from rest_framework.serializers import ValidationError


class AccountNotExist(ValidationError):
    pass


class InvalidAccountId(ValidationError):
    pass


class SameNameAccountExists(ValidationError):
    pass


class FundsTransferException(ValidationError):
    pass


class InsufficientFunds(FundsTransferException):
    pass


class CurrencyTransferNotSupported(FundsTransferException):
    pass


class SameAccountTransfersProhibited(FundsTransferException):
    pass


class IncorrectTransferAmount(FundsTransferException):
    pass
