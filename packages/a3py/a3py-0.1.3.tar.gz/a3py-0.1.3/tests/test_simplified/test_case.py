# -*- coding: utf-8 -*-
import unittest

from a3py.simplified import case


class T(unittest.TestCase):

    def test__snake2camel__success(self):
        self.assertEqual(case.snake2camel('phone'), 'Phone')
        self.assertEqual(case.snake2camel('phone_number'), 'PhoneNumber')
        self.assertEqual(case.snake2camel('p_n'), 'PN')

    def test__camel2snake__success(self):
        self.assertEqual(case.camel2snake('Phone'), 'phone')
        self.assertEqual(case.camel2snake('PhoneNumber'), 'phone_number')
        self.assertEqual(case.camel2snake('PN'), 'p_n')
