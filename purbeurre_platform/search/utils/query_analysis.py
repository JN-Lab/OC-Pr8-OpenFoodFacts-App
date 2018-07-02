#! /usr/bin/env python3
# coding: utf-8
import operator
from functools import reduce
from django.db.models import Q
from ..models import Product, Category

class QueryAnalysis:
    """
    This class groups all the methods to interact with the database during:
        -> Search process
    """

    def get_info_in_db(self, model, query):
        """
        This method gets in database the categories or products (max 6) according
        usr query. If there is any category or product, it returns None
        """
        
        words_query = query.lower().split()
        conditions = []
        for word in words_query:
            conditions.append(("name__icontains", word))
        q_object = [Q(x) for x in conditions]

        queryset = model.objects.filter(reduce(operator.or_, q_object))[:6]
        if queryset:
            return queryset
        else:
            return None

    def get_substitute_products_in_db(self, category_name, number):
        """
        This method gets substitute products from a category if there are
        enough products with an "a" nutriscore or None 
        """

        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(categories=category.id, nutriscore="a")[:number]
        if len(products) >= number:
            return products
        else:
            return None

    def get_selected_product(self, product_code):
        """
        This method gets all necessary information from a products thanks to its code
        """

        try:
            product = Product.objects.get(ref=product_code)
            return product
        except:
            return None

    def set_product_registered(self, product):
        pass

    def check_db_size(self):
        pass

    def select_non_registered_product(self):
        pass

    def delete_product_with_former_last_interaction(self):
        pass