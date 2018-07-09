#! /usr/bin/env python3
# coding: utf-8
import operator
import unicodedata
from functools import reduce
from django.db.models import Q
from ..models import Product, Category

class QueryAnalysis:
    """
    This class groups all the methods to interact with the database during:
        -> Search process
    """

    def get_search_selection(self, query):
        """
        This is the main method which coordinates all the actions in the search process
        inside the db
        """
        query = self._clean_query(query)
        check = self._get_info_in_db(Category, query)
        if check:
            categories = self._queryset_to_dict(check, "category")
            return categories
        else:
            check = self._get_info_in_db(Product, query)
            if check:
                products = self._queryset_to_dict(check, "product")
                return products
            else:
                return None

    def _clean_query(self, query):
        useless_terms = ['a', 'de', 'de', 'des', 'un', 'une', 'tout', 'tous', 'les',
                         'la', 'le', 'qui', 'que', 'quoi', 'ce', 'ces', 'sans', 'avec']
        
        # set query in lowercase
        query = query.lower()
        
        # Remove accents
        try:
            query = unicode(query, 'utf-8')
        except NameError:
            pass
        query = unicodedata.normalize('NFD', query)
        query = query.encode('ascii', 'ignore')
        query = query.decode('utf-8')
        query = str(query)

        # Delete useless terms in query
        query_list = query.split()
        clean_query_list = []
        for word in query_list:
            if word not in useless_terms:
                clean_query_list.append(word)

        query = ' '.join(clean_query_list)
        return query

    def _get_info_in_db(self, model, query):
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

    def _queryset_to_dict(self, queryset, typology):
        """
        This method transforms queryset get for precising search selection into a dictionnary
        """

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
                element["description"] = product.description
                element["image_url"] = product.picture
                dict_info["elements"].append(element)

        dict_info["number"] = len(dict_info["elements"])
        return dict_info

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

class SubstituteSelection:

    def get_substitue_products(self):
        pass

    def _get_products_from_products(self):
        pass

    def _get_products_from_categories(self):
        pass