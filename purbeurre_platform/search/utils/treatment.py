#! /usr/bin/env python3
# coding: utf-8

from .db_interactions import DBInteractions, SubstituteSelection
from .api_interactions import OpenFoodFactsInteractions

class Treatment:

    def __init__(self):
        self.query_analysis = DBInteractions()
        self.db_selection_to_substitute = SubstituteSelection()
        self.api_interactions = OpenFoodFactsInteractions()

    def get_choice_selection(self, query):

        db_info = self.query_analysis.get_search_selection(query)
        if db_info:
            return db_info
        else : 
            api_info = self.api_interactions.get_products_selection(query, 6)
            if api_info:
                return api_info
            else:
                return None

    def get_substitute_selection(self, element_type, type_name):
        db_info = self.db_selection_to_substitute.get_substitute_products_in_db(element_type, type_name)
        if db_info:
            return db_info
        else:
            api_info = self.api_interactions.get_substitute_products_from_api(element_type, type_name, 6)
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