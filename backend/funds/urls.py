from django.urls import path

from .views import AccountView, BalanceView, FundsTransferView, TransactionsHistoryView


urlpatterns = [
    path(
        'accounts/<str:sender_account_id>/transfer/<str:beneficiary_account_id>/',
        FundsTransferView.as_view(), name='transfer_funds'
    ),
    path(
        'transfers_history/<str:account_id>/',
        TransactionsHistoryView.as_view(), name='retrieve_funds_transfers_history'
    ),
    path('accounts/<str:account_id>/', BalanceView.as_view(), name='retrieve_account_balance'),
    path('accounts/', AccountView.as_view(), name='create_account'),
]
