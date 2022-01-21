from uuid import uuid4
from decimal import Decimal

from .abstract import AbstractFundsTransfer
from funds.types import CurrencyEnum
from funds.models import Account, FundsTransferHistory
from funds.exceptions import CurrencyTransferNotSupported, SameAccountTransfersProhibited, IncorrectTransferAmount


class InternalSystemFundsTransfer(AbstractFundsTransfer):
    """Specific AbstractFundsTransfer implementation for funds transfers within internal banking system."""
    def make_transfer(
            self,
            sender_account: Account,
            beneficiary_account: Account,
            amount: Decimal,
            currency: CurrencyEnum
    ) -> uuid4:
        """Making funds transfer from sender to beneficiary funds."""
        self._validate(amount=amount, currency=currency, sender_account=sender_account, beneficiary_account=beneficiary_account)

        # Concurrent transfers requests handling is implemented inside corresponding `withdraw` and `deposit` methods.
        sender_account.withdraw(amount)
        beneficiary_account.deposit(amount)

        return FundsTransferHistory.objects.create(
            sender=sender_account,
            beneficiary=beneficiary_account,
            amount=amount,
            currency=currency
        ).uuid

    @staticmethod
    def _validate(sender_account: Account, beneficiary_account: Account, currency: CurrencyEnum, amount: Decimal):
        """Validating funds transfer inputs according to business requirements."""
        # We could validate some inputs on serializer level, but also it makes sense to
        # keep transfer-related validations in one place (business logic module).
        if amount <= 0:
            raise IncorrectTransferAmount('Amount should be a decimal number greater than 0')
        if currency != CurrencyEnum.USD:
            raise CurrencyTransferNotSupported(
                f'Only transfers denominated in {CurrencyEnum.USD} are supported at the moment'
            )
        if sender_account.uuid == beneficiary_account.uuid:
            raise SameAccountTransfersProhibited('Transferring funds within the same funds is prohibited')
