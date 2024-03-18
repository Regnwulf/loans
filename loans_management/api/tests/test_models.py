from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from ..models import Loan, Payment


class LoanModelTestCase(TestCase):
    def setUp(self):
        self.loan = Loan.objects.create(
            nominal_value=Decimal('1000.00'),
            interest_rate=Decimal('0.79'),
            iof_rate=Decimal('0.005'),
            insurance_rate=Decimal('0.015'),
            request_date='2024-03-18',
            bank='Test Bank',
            client='Test Client',
        )
        Payment.objects.create(
            loan=self.loan, payment_date=timezone.now().date(), amount=Decimal('500.00'))
        Payment.objects.create(
            loan=self.loan, payment_date=timezone.now().date(), amount=Decimal('300.00'))

    def test_loan_creation_missing_required_field(self):
        with self.assertRaises(Exception):
            Loan.objects.create(
                interest_rate=Decimal('0.79'),
                iof_rate=Decimal('0.005'),
                insurance_rate=Decimal('0.015'),
                request_date='2024-03-18',
                bank='Test Bank',
                client='Test Client',
            )


class PaymentModelTestCase(TestCase):
    def setUp(self):
        self.loan = Loan.objects.create(
            nominal_value=Decimal('1000.00'),
            interest_rate=Decimal('0.79'),
            iof_rate=Decimal('0.005'),
            insurance_rate=Decimal('0.015'),
            request_date='2024-03-18',
            bank='Test Bank',
            client='Test Client',
        )

    def test_payment_creation(self):
        payment_date = timezone.now().date()
        amount = Decimal('500.00')

        payment = Payment.objects.create(
            loan=self.loan, payment_date=payment_date, amount=amount)
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.loan, self.loan)
        self.assertEqual(payment.payment_date, payment_date)
        self.assertEqual(payment.amount, amount)

    def test_payment_creation_without_loan(self):
        payment_date = timezone.now().date()
        amount = Decimal('500.00')

        with self.assertRaises(Exception):
            Payment.objects.create(payment_date=payment_date, amount=amount)
