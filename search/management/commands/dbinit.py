#! /usr/bin/env python3
# coding: utf-8
import requests
import math
import unicodedata
from django.core.management.base import BaseCommand
from ...models import Product, Category

class DBInit:
    """
    This class groups all the scripts to execute to populate the database with
    the initial datas.
    To objectives:
        -> Respect the limitations of 10k rows from freemium account on Heroku
        -> Get the most common datas in order to minimize API Call during navigation
    """
    
    def clean_db(self):
        """
        This public method deletes all the categories and products in db
        before populates it
        """
        categories = Category.objects.all()
        products = Product.objects.all()
        if categories:
            categories.delete()
        if products:
            products.delete()

        print("db clean process --> OK")

    def set_categories(self):
        """
        This public method realizes all the process to integrate the appropriate
        categories in the database
        """

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
        """
        This public method realizes all the process to integrate the appropriate
        products in the database
        """

        print("### Start Products Selection ###")

        products_per_page = 1000
        max_healthy_products = 6
        max_dirty_products = 6

        categories = Category.objects.all()
        for category in categories:
            print("looking for categories : {}".format(category.name))
            page_number = self._get_product_pages_number(category.total_products, products_per_page)
            page = 1
            healthy_product = 0
            dirty_products = 0
            while page <= page_number and (healthy_product < max_healthy_products or dirty_products < max_dirty_products):
                products_data = self._get_from_api_products_info_from_page_category(category.api_id, products_per_page, page )
                for product in products_data["products"]:
                    try:
                        print("looking for product : {}".format(product["product_name_fr"]))
                        if product["nutrition_grade_fr"] == "a" and healthy_product < max_healthy_products:
                            product["product_name_fr"] = self._clean_name(product["product_name_fr"])
                            self._inject_products(product)
                            healthy_product += 1
                            print("SUCCESS product {} injected".format(product["product_name_fr"]))
                        elif (product["nutrition_grade_fr"] == "d" or product["nutrition_grade_fr"] == "e") and dirty_products < max_dirty_products:
                            product["product_name_fr"] = self._clean_name(product["product_name_fr"])
                            self._inject_products(product)
                            dirty_products += 1
                            print("SUCCESS product {} injected".format(product["product_name_fr"]))
                    except:
                        pass
                page +=1
        
        print("### Selected Products Injected ###")
    
    def _get_categories_from_api(self):
        """
        This method requests the API to get all the categories
        """

        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        data = request.json()

        return data

    def _get_from_api_products_info_from_page_category(self, category, page_size, page):
        """
        This method requests from the API a page of products according a category 
        """

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
        """
        This method calculates the number of pages to get all the products
        from a category
        """

        page_number = math.ceil(total_products / products_per_page)
        return page_number

    def _count_healthy_products(self, products_list):
        """
        This method calculates the amount of products with a nutriscore "a" on
        product list
        """
        healthy_product = 0
        for product in products_list:
            try:
                if product["nutrition_grade_fr"] == "a":
                    healthy_product += 1
            except:
                pass

        return healthy_product
    
    def _inject_categories(self, category):
        """
        This method injects a category into the database
        """
        Category.objects.create(name=category["name"],
                                api_id=category["id"],
                                total_products=category["products"],
                                enough_good_nutriscore=True)

    def _inject_products(self, product):
        """
        This method injects a product with its categories depedencies
        into a database
        """
        product_exist = Product.objects.filter(name=product["product_name_fr"]).exists()
        if not product_exist:
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
        """
        This method cleans a name before inject it into the database
        """
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
    """
    This class describe the different actions to realize when the dbinit command
    is launched.
    """
    def handle(self, **options):
        db_init = DBInit()
        db_init.clean_db()
        db_init.set_categories()
        db_init.set_products()