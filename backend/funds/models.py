"""Data models."""

__all__ = ['Account', 'FundsTransferHistory']

import logging
from decimal import Decimal

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .types import CurrencyEnum
from .exceptions import InsufficientFunds
from root.models import AbstractBaseModel


class Account(AbstractBaseModel):
    """Represents information about financial funds and it's owner."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(
        max_digits=29,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.0'))],
        default=0.0
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyEnum.choices,
        default=CurrencyEnum.USD
    )

    def get_queryset(self):
        return self.__class__.objects.filter(uuid=self.uuid)

    def deposit(self, amount):
        logging.info(f'Depositing {amount} {self.currency} to funds `{self.uuid}`...')
        # Locking db record to handle same account deposit concurrent requests and making db responsible for increment.
        self.get_queryset().select_for_update().update(balance=F('balance') + amount)

    def withdraw(self, amount):
        logging.info(f'Withdrawing {amount} {self.currency} from funds `{self.uuid}`...')
        # Locking db record to handle same account withdraw concurrent requests.
        queryset = self.get_queryset().select_for_update()
        if amount > queryset.get().balance:
            raise InsufficientFunds('Insufficient funds balance')
        queryset.update(balance=F('balance') - amount)  # Making db responsible for balance decrement operation.

    class Meta:
        unique_together = (('name', 'owner'),)


class FundsTransferHistory(AbstractBaseModel):
    """Represents information about transactions history."""
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_senders')
    beneficiary = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_beneficiaries')
    amount = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
    currency = models.CharField(max_length=3)  # If funds currency got changed at some point, keep history immutable.

    class Meta:
        ordering = ['-created_at']
