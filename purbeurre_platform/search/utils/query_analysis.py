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

    def queryset_to_dict(self, queryset, typology):

        dict_info = {
            'type' : '',
            'number' : 0,
            'elements': []
        }


        if typology == "category":
            dict_info["type"] = "category"
            for category in queryset:
                element = {
                    'name' : '',
                    'ref' : '',
                    'nutriscore' : '',
                    'description' : '',
                    'image_url' : '' 
                }        
                element["name"] = category.name
                element["description"] = category.api_id
                dict_info["elements"].append(element)
        elif typology == "product":
            dict_info["type"] = "product"
            for product in queryset:
                element = {
                    'name' : '',
                    'ref' : '',
                    'nutriscore' : '',
                    'description' : '',
                    'image_url' : '' 
                }
                element["name"] = product.name
                element["ref"] = product.ref
                element["nutriscore"] = product.nutriscore
                element["image_url"] = product.picture
                dict_info["elements"].append(element)

        dict_info["number"] = len(dict_info["elements"])
        return dict_info


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