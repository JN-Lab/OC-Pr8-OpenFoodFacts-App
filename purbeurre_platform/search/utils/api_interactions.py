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
    
    def get_products_selection(self, query, max_numb):
        """
        This method coordinates severa methods from the class to give some example :
            -> If api sends back products, it cleaned them
            -> If selected product > wanted number, a process of selection is realized
            -> It returns the necessary dict at the end
        """

        data_from_api = self._get_products_from_api_brand_search(query)

        if data_from_api["count"] > 0:
            products_selected = self._select_appropriate_products(data_from_api, query)
            if products_selected["number"] > max_numb :
                self._select_by_product_name(products_selected, max_numb)
                self._select_by_nutriscore_value(products_selected, max_numb)
                self._select_by_image(products_selected, max_numb)
                self._select_by_description(products_selected, max_numb)
                self._select_by_random_way(products_selected, max_numb)
            return products_selected
        else:
            return None

    def get_substitute_products_from_api(self, element_type, type_name, max_numb):
        """
        This method coordinates all 
        """
        if element_type == "category":
            data_from_api = self._get_products_from_api_category_search(type_name)
        elif element_type == "product":
            # Maybe to optimize
            data_from_api = self._get_products_from_api_brand_search(type_name)

        if data_from_api["count"] > 0:
            products_selected = self._select_substitute_products(data_from_api)
            if products_selected["number"] > max_numb :
                self._select_by_product_name(products_selected, max_numb)
                self._select_by_nutriscore_value(products_selected, max_numb)
                self._select_by_image(products_selected, max_numb)
                self._select_by_description(products_selected, max_numb)
                self._select_by_random_way(products_selected, max_numb)
            return products_selected
        else:
            return None          

        
    def _get_products_from_api_brand_search(self, query):
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

        return data

    def _get_products_from_api_category_search(self, category_name):
        """
        This method requests all the products from a category
        """

        request = requests.get("https://fr.openfoodfacts.org/categorie/" + category_name + ".json")
        data = request.json()

        return data

    def _select_substitute_products(self, data):
        """
        This method gets the data from the API (products json linked to a category)
        and cleaned them to return only products:
            -> with a product name
            -> a nutriscore equal to "d" or "e"
            -> an image url
            -> a description
        """
        products_info = {
            'type' : 'product',
            'number' : 0,
            'elements': []
        }
        for product in data["products"]:
            element = {
                "name" : "",
                "ref" : "",
                "nutriscore" : "",
                "description" : "",
                "image_url" : "" 
            }
            try:
                if str(product["product_name_fr"]).split() and product["nutrition_grade_fr"] == "a":
                    element["name"] = product["product_name_fr"]
                    element["ref"] = product["code"]
                    element["nutriscore"] = product["nutrition_grade_fr"]
                    try:
                        element["description"] = product["generic_name_fr"]
                        element["image_url"] = product["image_url"]
                    except:
                        pass

                    products_info["elements"].append(element)
            except:
                pass

        products_info["number"] = len(products_info["elements"])

        return products_info

    def _select_appropriate_products(self, data, query):
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
            try:
                appropriate_name = test.match(product["product_name_fr"])
                nutriscore = product["nutrition_grade_fr"]
            
                if appropriate_name and nutriscore:
                    element = {
                        "name" : "",
                        "ref" : "",
                        "nutriscore" : "",
                        "description" : "",
                        "image_url" : "" 
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
            except:
                pass

        products_info["number"] = len(products_info["elements"])

        return products_info

    def _select_by_image(self, data, max_numb):
        """
        This method removes products without image url from products list
        if the number of products is > max_numb
        """
        elements_cleaned = []
        products_numb = data["number"]
        for product in data["elements"]:
            if not product["image_url"] and products_numb > max_numb:
                products_numb -= 1
            else:
                elements_cleaned.append(product)
        data["elements"] = elements_cleaned
        data["number"] = products_numb
        return data

    def _select_by_description(self, data, max_numb):
        """
        This method removes products without description from products list
        if the number of products is > max_numb
        """
        elements_cleaned = []
        products_numb = data["number"]
        for product in data["elements"]:
            if not product["description"] and products_numb > max_numb:
                products_numb -= 1
            else:
                elements_cleaned.append(product)
        data["elements"] = elements_cleaned
        data["number"] = products_numb
        return data

    def _select_by_nutriscore_value(self, data, max_numb):
        """
        This method removes products with good nutriscore from products list
        if the number of products is > max_numb
        """
        elements_cleaned = []
        products_numb = data["number"]
        for product in data["elements"]:
            if product["nutriscore"] == "a" and products_numb > max_numb:
                products_numb -= 1
            else:
                elements_cleaned.append(product)
        data["elements"] = elements_cleaned
        data["number"] = products_numb
        return data

    def _select_by_random_way(self, data, max_numb):
        """
        This method selects on random way several products defines by max_numb
        argument if the length of the products is > max_numb 
        """
        if len(data["elements"]) > max_numb:
            random_product = random.sample(data["elements"], max_numb)
            data["elements"] = random_product

        data["number"] = len(data["elements"])

        return data

    def _select_by_product_name(self, data, max_numb):
        """
        This method removes products if a similar product name had already been accepted
        """
        elements_cleaned = []
        products_name_accepted = []
        products_numb = data["number"]
        for product in data["elements"]:
            if product["name"].lower() in products_name_accepted and products_numb > max_numb:
                products_numb -= 1
            else:
                elements_cleaned.append(product)
                products_name_accepted.append(product["name"].lower())

        data["elements"] = elements_cleaned
        data["number"] = products_numb
        return data
