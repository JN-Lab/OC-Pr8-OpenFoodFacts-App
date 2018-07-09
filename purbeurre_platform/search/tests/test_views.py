#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.urls import reverse
from ..views import index

class IndexPageTestCase(TestCase):

    def test_index_page_status(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ChoicePageTestCase(TestCase):

    def test_choice_page(self, type, type_id):
        pass