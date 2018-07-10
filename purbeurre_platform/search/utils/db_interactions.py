#! /usr/bin/env python3
# coding: utf-8
import operator
import unicodedata
from functools import reduce
from django.db.models import Q
from ..models import Product, Category

class DBInteractions:
    """
    This class groups all the methods to interact with the database during:
        -> Search process
    """

    ## PUBLIC METHODS ##
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

    def get_substitute_products_in_db(self, element_type, type_name):
        """
        This is the main method which coordinates all the actions to find substitue
        products inside the db
        """
        if element_type == "category":
            check = self._get_healthy_products_from_categories(type_name)
        elif element_type == "product":
            check = self._get_healthy_products_from_products(type_name)
        
        if check:
            products = self._queryset_to_dict(check, "product")
            return products
        else:
            return None
            

    ## PRIVATE METHODS ##
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

    def _get_selected_product(self, product_code):
        """
        This method gets all necessary information from a products thanks to its code
        """

        try:
            product = Product.objects.get(ref=product_code)
            return product
        except:
            return None



    def _get_healthy_products_from_products(self, product_name):
        try:
            # We get product info
            product = Product.objects.get(name=product_name)
            # We select the appropriate category associated by choosing the cat with the minimum size
            total_product = -1
            choosen_category = ""
            for category in product.categories.all():
                if category.total_products < total_product or total_product < 0:
                    total_product = category.total_products
                    choosen_category = category.api_id
            # We select the products to substitute thankts to the choosen_category
            products = self._get_healthy_products_from_categories(choosen_category)
            return products

        except:
            return None

    def _get_healthy_products_from_categories(self, category_name):
        """
        This method gets dirty products to subsititude from a selected category:
            -> we use api_id value because it is cleaner than name
        """
        try:
            category = Category.objects.get(api_id=category_name)
            products = Product.objects.filter(Q(categories=category.id) & Q(nutriscore="a"))[:6]
            return products
        except:
            return None

