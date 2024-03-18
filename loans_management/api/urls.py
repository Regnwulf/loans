from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, PaymentViewSet, OutstandingBalanceAPIView


router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('outstanding_balance/', OutstandingBalanceAPIView.as_view(),
         name='total-outstanding-balance'),
    path('outstanding_balance/<str:identifier>/',
         OutstandingBalanceAPIView.as_view(), name='outstanding_balance'),

]
