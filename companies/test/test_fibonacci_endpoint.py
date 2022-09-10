from django.urls import reverse
from django.test import TestCase
from rest_framework import status


get_fibonacci_url = lambda n: reverse('fibonacci', args=(n,))


class FibonacciTests(TestCase):
    def test_fibonacci_returns_result_when_4(self):
        res = self.client.get(get_fibonacci_url(n=4))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['fibonacci_result'], 3)

    def test_fibonacci_returns_result_when_2(self):
        res = self.client.get(get_fibonacci_url(n=2))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['fibonacci_result'], 1)

    def test_fibonacci_returns_result_when_negative_number(self):
        res = self.client.get(get_fibonacci_url(n=-2))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['error'], 'negative_number')
