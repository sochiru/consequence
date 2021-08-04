"""API URL Configuration"""
from django.conf import settings
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .authentication.view import AuthLinkView, AuthCallbackView, UserLogoutView
from .user.view.user import UserRegisterView
from .cards.view import CardsViewSet, CardDetailViewSet, CardsTransactionsViewSet, CardsTransactionsPendingViewSet
from .accounts.view import AccountsListView, AccountsDetailView, AccountsDetailBalanceView, AccountsDetailTransactionsView, AccountsDetailTransactionsPendingView


urlpatterns = [
    path('jwt', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('jwt/refresh', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/logout', UserLogoutView.as_view(), name="logout"),
    path('auth/link', AuthLinkView.as_view(), name='auth-link'),
    path('auth/callback', AuthCallbackView.as_view(), name='exchange-code'),
    path('users/register', UserRegisterView.as_view(), name='user-register'),

    path('cards', CardsViewSet.as_view({'get': 'list'}), name='cards-list'),
    path('cards/<str:card_id>', CardDetailViewSet.as_view({'get': 'retrieve'}), name='cards-detail'),
    path('cards/<str:card_id>/transactions',
         CardsTransactionsViewSet.as_view({'get': 'transactions'}), name='card-transactions'),
    path('cards/<str:card_id>/transactions/pending',
         CardsTransactionsPendingViewSet.as_view({'get': 'transactions_pending'}), name='card-transactions-pending'),

    path('accounts', AccountsListView.as_view(), name='accounts_list'),
    path('accounts/<str:account_id>', AccountsDetailView.as_view(), name='account_detail'),
    path('accounts/<str:account_id>/balance', AccountsDetailBalanceView.as_view(), name='account_detail_balance'),
    path('accounts/<str:account_id>/transactions', AccountsDetailTransactionsView.as_view(), name='account_detail_transactions'),
    path('accounts/<str:account_id>/transactions/pending',
         AccountsDetailTransactionsPendingView.as_view(), name='account_detail_transactions_pending'),
]

router = SimpleRouter(trailing_slash=False)
if settings.DEBUG:
    router = DefaultRouter(trailing_slash=False)

router.register('cards/<pk:card_id>/transactions/pending', CardsTransactionsPendingViewSet,
                basename='cards-detail-transactions-pending')
# router.register('cards/webhook', CardsHookViewSet, basename='cards-hook')


urlpatterns += router.urls
