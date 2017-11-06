from django.test import TestCase
from .models import Module


# Create your tests here.
class SodTestCase(TestCase):
    def test_models_test(self):
        """Проверка, что все тестирование работает"""
        self.assertEqual("kek", "kek")