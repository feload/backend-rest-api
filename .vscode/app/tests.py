from django.test import TestCase
from .calc import add

class CalcTests(TestCase):

    '''Test functions must start with "test"'''
    def test_add_numbers(self):
        '''Test that add two numbers together.'''
        self.assertEqual(add(3,8), 11)
