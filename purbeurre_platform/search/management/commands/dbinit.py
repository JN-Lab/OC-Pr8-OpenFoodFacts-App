#! /usr/bin/env python3
# coding: utf-8
import requests
import math
import unicodedata
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

        print("db clean process --> OK")

    def set_categories(self):

        min_product_number = 150
        max_product_number = 1000
        products_per_page = 1000
        min_healthy_products = 6

        print("### Start Categories Selection ###")
        categories = self._get_categories_from_api()

        for category in categories["tags"]:
            print("looking for category : {}".format(category["name"]))
            healthy_products = 0
            if category["products"] > min_product_number and category["products"] < max_product_number:
                print("HEY -> Maybe this one")
                page_number = self._get_product_pages_number(category["products"], products_per_page)
                page = 1
                while page <= page_number and healthy_products < min_healthy_products:
                    print("Page : {} | Total Pages : {}".format(page, page_number))
                    products_data = self._get_from_api_products_info_from_page_category(category["id"], products_per_page, page)
                    healthy_products += self._count_healthy_products(products_data["products"])
                    page +=1
                    print("healthy products found : {}".format(healthy_products))

            if healthy_products >= min_healthy_products:
                category["name"] = self._clean_name(category["name"])
                self._inject_categories(category)
                print("SUCCESS : category injected : {}".format(category["name"]))
        
        print("### Selected Categories Injected ###")

    def set_products(self):

        print("### Start Products Selection ###")

        products_per_page = 1000

        categories = Category.objects.all()
        for category in categories:
            print("looking for categories : {}".format(category.name))
            page_number = self._get_product_pages_number(category.total_products, products_per_page)
            page = 1
            for page in range(page_number + 1):
                products_data = self._get_from_api_products_info_from_page_category(category.api_id, products_per_page, page )
                for product in products_data["products"]:
                    print("looking for product : {}".format(product["product_name_fr"]))
                    try:
                        if product["nutrition_grade_fr"] == "a":
                            product["product_name_fr"] = self._clean_name(product["product_name_fr"])
                            self._inject_products(product)
                            print("SUCCESS product {} injected".format(product["product_name_fr"]))
                    except:
                        pass

        print("### Selected Products Injected ###")
    
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
        Category.objects.create(name=category["name"],
                                api_id=category["id"],
                                total_products=category["products"],
                                enough_good_nutriscore=True)

    def _inject_products(self, product):
        new_product = Product.objects.create(name=product["product_name_fr"],
                               ref=product["code"],
                               nutriscore=product["nutrition_grade_fr"],
                               picture=product["image_url"],
                               description=product["generic_name_fr"])
            
        for category in product["categories_hierarchy"]:
            try:
                cat_in_db = Category.objects.get(api_id=category) 
                new_product.categories.add(cat_in_db)
            except:
                pass

    def _clean_name(self, name):
        name = name.lower()
        try:
            name = unicode(name, 'utf-8')
        except NameError:
            pass
        name = unicodedata.normalize('NFD', name)
        name = name.encode('ascii', 'ignore')
        name = name.decode('utf-8')
        return str(name)


class Command(BaseCommand):
    def handle(self, **options):
        db_init = DBInit()
        db_init.clean_db()
        db_init.set_categories()