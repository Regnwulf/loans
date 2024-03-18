from decimal import Decimal

from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip_address, client=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(loan__client=self.request.user)


class OutstandingBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, identifier=None):
        if identifier:
            loan = self.get_loan(identifier)
            outstanding_balance = self.calculate_outstanding_balance(loan)
            return Response({'outstanding_balance': outstanding_balance})
        else:
            total_outstanding_balance = self.calculate_total_outstanding_balance(
                request.user)
            return Response({'total_outstanding_balance': total_outstanding_balance})

    def calculate_outstanding_balance(self, loan):
        total_payments = self.calculate_total_payments(loan)
        total_interest = self.calculate_total_interest(loan)
        total_iof = loan.iof_rate * loan.nominal_value
        total_insurance = loan.insurance_rate * loan.nominal_value
        outstanding_balance = loan.nominal_value + total_interest + \
            total_iof + total_insurance - total_payments
        return round(outstanding_balance, 2)

    def calculate_total_payments(self, loan):
        total_payments = loan.payments.aggregate(total_payments=Sum('amount'))[
            'total_payments'] or Decimal('0.00')
        return total_payments

    def calculate_total_interest(self, loan):
        monthly_interest_rate = loan.interest_rate / Decimal(100)
        total_interest = loan.nominal_value * \
            monthly_interest_rate * loan.payments.count()
        return total_interest

    def get_loan(self, identifier):
        return Loan.objects.get(identifier=identifier, client=self.request.user)

    def calculate_total_outstanding_balance(self, user):
        total_outstanding_balance = Decimal('0.00')
        loans = Loan.objects.filter(client=user)
        for loan in loans:
            total_outstanding_balance += self.calculate_outstanding_balance(
                loan)
        return round(total_outstanding_balance, 2)
