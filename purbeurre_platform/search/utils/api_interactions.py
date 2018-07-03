#! /usr/bin/env python3
# coding: utf-8

import re
import random
import requests

class OpenFoodFactsInteractions:
    """
    This class groups all the methods to get necessary informations from
    OpenFoodFacts API during search process. The different actions:
            -> Request the API by using a search request on brands
            -> Clean Json
            -> Get the 6 (max) more appropriate product
            -> returns a list of dict : (products)

    products_info = {
            'type' : 'product',
            'number' : 0,
            'elements': [
                {
                    'name' : '',
                    'ref' : '',
                    'nutriscore' : '',
                    'description' : '',
                    'image_url' : '' 
                },
                {
                    'name' : '',
                    'ref' : '',
                    'nutriscore' : '',
                    'description' : '',
                    'image_url' : '' 
                },
                ...
            ]
        }
    """
    
    def get_products_with_brand(self, query):
        """
        This method gets all the products from the API linked to the brands asked by the user (query)
        If there is no product -> return None
        If there is product:
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
    
    def select_appropriate_products(self, data, query):
        """
        This method gets the data from API and cleaned them to return only
        products
            -> where the query matchs with the product name
            -> with a nutriscore 
        """
        products_info = {
            'type' : 'product',
            'number' : 0,
            'elements': []
        }

        test = re.compile(r".*%s.*" % query, re.IGNORECASE)
        
        for product in data["products"]:
            appropriate_name = test.match(product["product_name_fr"])
            nutriscore = product["nutrition_grade_fr"]
        
            if appropriate_name and nutriscore:
                element = {
                    'name' : '',
                    'ref' : '',
                    'nutriscore' : '',
                    'description' : '',
                    'image_url' : '' 
                }
                element["name"] = product["product_name_fr"]
                element["nutriscore"] = nutriscore
                element["ref"] = product["code"]
                try:
                    element["description"] = product["generic_name_fr"]
                    element["image_url"] = product["image_url"]
                except:
                    pass

                products_info["elements"].append(element)

        products_info["number"] = len(products_info["elements"])

        return products_info

    def select_by_image(self, data, max_numb):
        """
        This method removes products without image url from products list
        if the number of products is > max_numb
        """
        for product in data["elements"]:
            if not product["image_url"] and len(data["elements"]) > max_numb:
                data["elements"].remove(product)

        return data

    def select_by_description(self, data, max_numb):
        """
        This method removes products without description from products list
        if the number of products is > max_numb
        """
        for product in data["elements"]:
            if not product["description"] and len(data["elements"]) > max_numb:
                data["elements"].remove(product)

        return data

    def select_by_nutriscore_value(self, data, max_numb):
        """
        This method removes products with good nutriscore from products list
        if the number of products is > max_numb
        """
        for product in data["elements"]:
            if product["nutriscore"] == "a" and len(data["elements"]) > max_numb:
                data["elements"].remove(product)

        return data

    def select_by_random_way(self, data, max_numb):
        """
        This method selects on random way several products defines by max_numb
        argument if the length of the products is > max_numb 
        """
        if len(data["elements"]) > max_numb:
            random_product = random.sample(data["elements"], max_numb)
            data["elements"] = random_product

        return data

    def get_products_from_api(self, query, max_numb):
        """
        This method coordinates all the methods from the class:
            -> It gets json from the API accoding the user query (search by brand)
            -> If api sends back products, it cleaned them
            -> If selected product > wanted number, a process of selection is realized
            -> It returns the necessary dict at the end
        """
        api_data = self.get_products_with_brand(query)
        if api_data["count"] > 0:
            products_selected = self.select_appropriate_products(api_data, query)
            if products_selected["number"] > max_numb :
                self.select_by_nutriscore_value(products_selected, max_numb)
                self.select_by_image(products_selected, max_numb)
                self.select_by_description(products_selected, max_numb)
                self.select_by_random_way(products_selected, max_numb)
            return products_selected
        else:
            return None