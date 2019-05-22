from django.test import TestCase
from .calc import add, substract

class CalcTest(TestCase):

    '''Test functions names should start with "test"'''
    def test_add(self):
        '''Test add two numbers'''
        self.assertEqual(add(3,5), 8)

    def test_substract(self):
        '''Test substract two numbers'''
        self.assertEqual(substract(3,5), -2)