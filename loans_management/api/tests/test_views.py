from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from ..models import Loan, Payment
from ..views import OutstandingBalanceAPIView


class LoanViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_get_loan_list(self):
        self.client.force_authenticate(user=self.user)
        self.first_loan = Loan.objects.create(
            nominal_value=1000.95, interest_rate=0.05, bank='Test Bank 1', client=self.user)
        self.second_loan = Loan.objects.create(
            nominal_value=2000.95, interest_rate=0.07, bank='Test Bank 2', client=self.user)
        response = self.client.get('/api/loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_loan(self):
        self.client.force_authenticate(user=self.user)
        loan_data = {
            'nominal_value': 3000.95,
            'interest_rate': 0.06,
            'iof_rate': 0.06,
            'insurance_rate': 0.03,
            'request_date': '2024-03-18',
            'bank': 'Test Bank 3',
            'client': 'testuser'
        }
        response = self.client.post('/api/loans/', loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Loan.objects.filter(bank='Test Bank 3').exists())
        self.assertEqual(response.data['nominal_value'], Decimal('3000.95'))
        self.assertEqual(response.data['interest_rate'], Decimal('0.06'))
        self.assertEqual(response.data['iof_rate'], Decimal('0.06000'))
        self.assertEqual(response.data['insurance_rate'], Decimal('0.03000'))
        self.assertEqual(response.data['request_date'], '2024-03-18')
        self.assertEqual(response.data['bank'], 'Test Bank 3')
        self.assertEqual(response.data['client'], 'testuser')

    def test_create_loan_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/loans/', {'interest_rate': 0.05, 'bank': 'Test Bank'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nominal_value', response.data,
                      'Error message should indicate missing nominal value field')


class PaymentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.loan = Loan.objects.create(
            nominal_value=1000.95, interest_rate=0.05, bank='Test Bank 1', client=self.user)
        self.fist_payment = Payment.objects.create(
            loan=self.loan, payment_date='2022-03-20', amount=500.95)
        self.second_payment = Payment.objects.create(
            loan=self.loan, payment_date='2022-03-25', amount=1000.95)

    def test_get_payment_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_payment(self):
        self.client.force_authenticate(user=self.user)
        payment_data = {
            'loan': self.loan.id,
            'payment_date': '2022-03-30',
            'amount': 500.95
        }
        response = self.client.post(
            '/api/payments/', payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['loan'], self.loan.id)
        self.assertEqual(response.data['payment_date'], '2022-03-30')
        self.assertEqual(response.data['amount'], Decimal('500.95'))

    def test_create_payment_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_payment_data = {
            'payment_date': '2022-03-30',
            'amount': 500.95
        }
        response = self.client.post(
            '/api/payments/', invalid_payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OutstandingBalanceAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='test_user', password='test_password')
        self.loan = Loan.objects.create(
            nominal_value=Decimal('1000'), interest_rate=Decimal('0.05'), bank='Test Bank', client=self.user)
        Payment.objects.create(loan=self.loan, amount=500,
                               payment_date=timezone.now().date())
        Payment.objects.create(loan=self.loan, amount=300,
                               payment_date=timezone.now().date())

    def test_get_outstanding_balance_with_identifier(self):
        request = self.factory.get('/api/outstanding_balance/1/')
        force_authenticate(request, user=self.user)
        with patch('api.views.OutstandingBalanceAPIView.get_loan') as mock_get_loan:
            mock_get_loan.return_value = self.loan
            view = OutstandingBalanceAPIView.as_view()
            response = view(request, identifier='1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('outstanding_balance', response.data)

    def test_get_total_outstanding_balance(self):
        request = self.factory.get('/api/outstanding_balance/')
        force_authenticate(request, user=self.user)
        view = OutstandingBalanceAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_outstanding_balance', response.data)
