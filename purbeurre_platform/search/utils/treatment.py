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

    def get_substitute_products(self):
        pass
    def get_registered_products(self):
        pass
    def register_product(self):
        pass