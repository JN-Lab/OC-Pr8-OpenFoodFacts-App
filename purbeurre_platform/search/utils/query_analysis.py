#! /usr/bin/env python3
# coding: utf-8
import operator
from functools import reduce
from django.db.models import Q
from ..models import Product, Category

class QueryAnalysis:
    """
    This class groups all the methods to check if the search terms asked
    by the user is linked to a product or a category registered in the database
    """

    def get_info_in_db(self, model, query):
        """
        This method checked in database (Category or Product models) if there is 
        one or several appropriate products according the user query
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
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(categories=category.id, nutriscore="a")[:number]
        if len(products) >= number:
            return products
        else:
            return None

    def get_selected_product(self, product_name):
        pass

    def set_product_registered(self, product):
        pass

    def check_db_size(self):
        pass

    def select_non_registered_product(self):
        pass

    def delete_product_with_former_last_interaction(self):
        pass