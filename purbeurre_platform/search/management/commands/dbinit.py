#! /usr/bin/env python3
# coding: utf-8
import requests
import math
from django.core.management.base import BaseCommand
from ...models import Product, Category

class DBInit:
    
    def clean_db(self):
        categories = Category.objects.all()
        products = Product.objects.all()
        if categories:
            categories.delete()
        if products:
            products.delete()

    def set_categories(self):

        min_product_number = 150
        max_product_number = 1000
        products_per_page = 1000

        categories = self._get_categories_from_api()
        for category in categories["tags"]:
            min_healthy_products = 0
            if category["products"] > min_product_number and category["products"] < max_product_number:
                page_number = self._get_product_pages_number(category["products"], products_per_page)
                page = 1
                while page <= page_number or min_healthy_products < 12:
                    products_data = self._get_from_api_products_info_from_page_category(category["id"], products_per_page, page)
                    min_healthy_products += self._count_healthy_products(products_data["products"])
                    page +=1

            if min_healthy_products >= 12:
                self._inject_categories(category)
    
    def _get_categories_from_api(self):

        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        data = request.json()

        return data

    def _get_from_api_products_info_from_page_category(self, category, page_size, page):

        payload = {
            'action' : 'process',
            'tagtype_0' : 'categories',
            'tag_contains_0' : 'contains',
            'tag_0' : category,
            'page_size' : page_size,
            'page' : page,
            'json' : '1'
        }

        request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
        data = request.json()

        return data

    def _get_product_pages_number(self, total_products, products_per_page):

        page_number = math.ceil(total_products / products_per_page)
        return page_number

    def _count_healthy_products(self, products_list):
        healthy_product = 0
        for product in products_list:
            try:
                if product["nutrition_grade_fr"] == "a":
                    healthy_product += 1
            except:
                pass

        return healthy_product
    
    def _inject_categories(self, category):
        Category.objects.create(name=category["name"].lower(),
                                api_id=category["id"].lower(),
                                total_products=category["products"],
                                enough_good_nutriscore=True)


class Command(BaseCommand):
    def handle(self, **options):
        db_init = DBInit()
        db_init.clean_db()
        db_init.set_categories()