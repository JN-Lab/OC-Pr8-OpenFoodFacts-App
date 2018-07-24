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

    def get_registered_products(self, username):
        """
        This method just gets the method in DBInteractions class to get the registered products.
        It is just to deal only with Treatment class in views.
        Tests are realized in test_db_interactions.py
        """

        products = self.db_interactions.get_products_registered(username)
        return products

    def register_product(self, username, product_ref):
        """
        This is the main method to register a product to a user. The are many steps:
        -> We check if the total row in db is > to 8500
            -> If it is superior, we delete the product wich has the oldest last_interactions
                and which is not registered by a user
        -> We check if product exist in db (if not, we add it)
        -> We add the product to the user in the association table
        -> If the product is registered, we return a positive status = "registered"

        In the case where we don't find a product which is not registered by a user in the
        database and the volume of rows is > to 8500 -> any registration is done and we return
        a negative status = "database full"
        """

        status = ""
        rows = self.db_interactions.count_global_rows_in_db()
        db_ok = self.db_interactions.check_db_for_registration(rows)

        if db_ok:
            product_in_db = self.db_interactions.check_product_existence_in_db(product_ref)
            if not product_in_db:
                product_info = self.get_selected_product(product_ref)
                if product_info:
                    self.db_interactions.set_product_for_user_registration(product_info)
                else:
                    status = "database full"
            self.db_interactions.save_product_for_user(username, product_ref)
            status = "registered"
        else:
            status = "database full"

        return status