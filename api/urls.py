from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.saving_views import Savings, SavingDetail
from .views.trans_views import Transactions, TransactionDetail

urlpatterns = [
	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),

    # User routes
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),

    # Savings routes
    path('savings/', Savings.as_view(), name='savings'),
    path('savings/<int:pk>', SavingDetail.as_view(), name='saving_detail'),

    # transaction routes
    path('transactions/', Transactions.as_view(), name='transactions'),
    path('transactions/<int:pk>', TransactionDetail.as_view(), name='transaction_detail'),
]
