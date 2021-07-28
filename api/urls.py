"""API URL Configuration"""
from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .user.view.user import UserRegisterView
from .cards.view import CardsListView, CardsDetailView, CardsDetailBalanceView, CardsDetailTransactionsView,\
    CardsDetailTransactionsPendingView
from .accounts.view import AccountsListView, AccountsDetailView, AccountsDetailBalanceView, AccountsDetailTransactionsView, AccountsDetailTransactionsPendingView


urlpatterns = [
    path('auth', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register', UserRegisterView.as_view(), name='user_register'),
    path('cards', CardsListView.as_view(), name='cards_list'),
    path('cards/<str:card_id>', CardsDetailView.as_view(), name='card_detail'),
    path('cards/<str:card_id>/balance', CardsDetailBalanceView.as_view(), name='card_detail_balance'),
    path('cards/<str:card_id>/transactions', CardsDetailTransactionsView.as_view(), name='card_detail_transactions'),
    path('cards/<str:card_id>/transactions/pending',
         CardsDetailTransactionsPendingView.as_view(), name='card_detail_transactions_pending'),

    path('accounts', AccountsListView.as_view(), name='accounts_list'),
    path('accounts/<str:account_id>', AccountsDetailView.as_view(), name='account_detail'),
    path('accounts/<str:account_id>/balance', AccountsDetailBalanceView.as_view(), name='account_detail_balance'),
    path('accounts/<str:account_id>/transactions', AccountsDetailTransactionsView.as_view(), name='account_detail_transactions'),
    path('accounts/<str:account_id>/transactions/pending',
         AccountsDetailTransactionsPendingView.as_view(), name='account_detail_transactions_pending'),
]