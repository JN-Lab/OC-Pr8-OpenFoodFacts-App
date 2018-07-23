#! /usr/bin/env python3
# coding: utf-8

from .db_interactions import DBInteractions
from .api_interactions import OpenFoodFactsInteractions

class Treatment:

    def __init__(self):
        self.db_interactions = DBInteractions()
        self.api_interactions = OpenFoodFactsInteractions()

    def get_choice_selection(self, query):

        db_info = self.db_interactions.get_search_selection(query)
        if db_info:
            return db_info
        else : 
            api_info = self.api_interactions.get_products_selection(query, 6)
            if api_info:
                return api_info
            else:
                return None

    def get_substitute_selection(self, element_type, info_id):
        db_info = self.db_interactions.get_substitute_products_in_db(element_type, info_id)
        if db_info:
            return db_info
        else:
            api_info = self.api_interactions.get_substitute_products_from_api(element_type, info_id, 6)
            if api_info:
                return api_info
            else:
                return None

    def get_selected_product(self, product_ref):
        # Need to evolve the method to see if it is a product already registered by the user
        product_info = self.api_interactions.get_selected_product(product_ref)
        if product_info:
            return product_info
        else:
            return None

    def get_registered_products(self):
        pass

    def register_product(self, username, product_info):
        """
        This method just gets the method in DBInteractions class to register a product.
        It is just to deal only with Treatment class in views.
        """
        self.db_interactions.set_register_product_to_user(username, product_info)
        