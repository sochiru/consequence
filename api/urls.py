"""API URL Configuration"""
from django.conf import settings
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .authentication.view import AuthLinkView, AuthCallbackView, UserLogoutView
from .user.view.user import UserChangePasswordView, UserRegisterView, UserInfoViewSet
from .cards.view import CardsViewSet, CardDetailViewSet, CardsTransactionsViewSet, CardsTransactionsPendingViewSet
from .accounts.view import AccountsViewSet, AccountDetailViewSet, AccountTransactionsViewSet, AccountTransactionsPendingViewSet, AccountsWebhook


urlpatterns = [
    path('jwt', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('jwt/refresh', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/logout', UserLogoutView.as_view(), name="logout"),
    path('auth/link', AuthLinkView.as_view(), name='auth-link'),
    path('auth/callback', AuthCallbackView.as_view(), name='exchange-code'),
    path('me', UserInfoViewSet.as_view(), name='user-info'),
    path('change-password', UserChangePasswordView.as_view(), name='user-change-password'),
    path('users/register', UserRegisterView.as_view(), name='user-register'),

    path('cards', CardsViewSet.as_view({'get': 'list'}), name='cards-list'),
    path('cards/<str:card_id>', CardDetailViewSet.as_view({'get': 'retrieve'}), name='card-detail'),
    path('cards/<str:card_id>/transactions',
         CardsTransactionsViewSet.as_view({'get': 'list'}), name='card-transactions'),
    path('cards/<str:card_id>/transactions/pending',
         CardsTransactionsPendingViewSet.as_view({'get': 'list'}), name='card-transactions-pending'),

    path('accounts', AccountsViewSet.as_view({'get': 'list'}), name='accounts-list'),
    path('accounts/<str:account_id>', AccountDetailViewSet.as_view({'get': 'retrieve'}), name='account-detail'),
    path('accounts/<str:account_id>/transactions',
         AccountTransactionsViewSet.as_view({'get': 'list'}), name='account-transactions'),
    path('accounts/<str:account_id>/transactions/pending',
         AccountTransactionsPendingViewSet.as_view({'get': 'list'}), name='account-transactions-pending'),

    path('webhook/accounts', AccountsWebhook.as_view(), name='accounts-webhook'),

    # path('accounts', AccountsListView.as_view(), name='accounts_list'),
    # path('accounts/<str:account_id>', AccountsDetailView.as_view(), name='account_detail'),
    # path('accounts/<str:account_id>/balance', AccountsDetailBalanceView.as_view(), name='account_detail_balance'),
    # path('accounts/<str:account_id>/transactions', AccountsDetailTransactionsView.as_view(), name='account_detail_transactions'),
    # path('accounts/<str:account_id>/transactions/pending',
    #      AccountsDetailTransactionsPendingView.as_view(), name='account_detail_transactions_pending'),
]

router = SimpleRouter(trailing_slash=False)
if settings.DEBUG:
    router = DefaultRouter(trailing_slash=False)

router.register('cards/<pk:card_id>/transactions/pending', CardsTransactionsPendingViewSet,
                basename='cards-detail-transactions-pending')
# router.register('cards/webhook', CardsHookViewSet, basename='cards-hook')


urlpatterns += router.urls
