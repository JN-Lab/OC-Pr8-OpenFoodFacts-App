#! /usr/bin/env python3
# coding: utf-8

import requests

class OpenFoodFactsInteractions:
    """
    This class groups all the methods to get necessary informations from
    OpenFoodFacts API during search process
    """
    
    def get_products_with_brand(self, query):
        """
        This method gets all the products from the API linked to the brands asked by the user (query)
        If there is no product -> return None
        If there is product:
            -> Clean Json
            -> Get the 6 more appropriate product
            -> returns a list of 6 dict : (products)
        """

        payload = {
            'action' : 'process',
            'json' : '1',
            'tagtype_0' : 'brands',
            'tag_contains_0' : 'contains',
            'tag_0' : query,
            'page_size' : '150',
            'page' : '1'
        }

        request = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
        data = request.json()

        if data["count"] > 0:
            return data
        else:
            return None
    
    def clean_response_brand(self, data):

        product_info = {
            'injection' : True,
            'url' : '',
            'nutrition_grade_fr' : '',
            'product_name_fr' :'',
            'code' : '',
        }

        pass

    def select_appropriate_products(self, response):
        pass

    def get_products_from_api(self, query):
        pass
        # Mise en histoire des 2 requêtes au-dessus
        # Retourne un dict