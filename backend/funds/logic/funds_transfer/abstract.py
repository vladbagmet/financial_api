from uuid import uuid4
from decimal import Decimal

from abc import ABC, abstractmethod

from funds.models import Account
from funds.types import CurrencyEnum


class AbstractFundsTransfer(ABC):
    """Defines funds transferring interface for subclasses."""

    @abstractmethod
    def make_transfer(
            self,
            sender_account: Account,
            beneficiary_account: Account,
            amount: Decimal,
            currency: CurrencyEnum
    ) -> uuid4:
        """Defines inputs and outputs for funds transferring processing."""
        pass
