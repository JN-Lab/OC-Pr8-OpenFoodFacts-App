#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from ..utils.api_interactions import OpenFoodFactsInteractions

class TestApiInteractions(TestCase):

    def test_get_products_with_brand_success(self):
        query = "nutella"
        pass