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

    def register_product(self, username, product_info):
        """
        This method just gets the method in DBInteractions class to register a product.
        It is just to deal only with Treatment class in views.
        Tests are realized in test_db_interactions.py
        """
        status = self.db_interactions.set_register_product_to_user(username, product_info)
        return status

        # status = ""
        # db_ok = False
        # rows = self.db_interactions._count_global_rows_in_db()

        ## db_ok = self.db_interactions.check_db_for_registration()
        # if rows > 8500:
        #     products = Product.objects.all().order_by('last_interaction')
        #     product_checked = 0
        #     while not db_ok and product_checked < products.count() - 1:
        #         product = products[product_checked]
        #         if not product.users.all().exists():
        #             product.delete()
        #             db_ok = True
        #         else:
        #             product_checked += 1
        # else:
        #     db_ok = True
        
        # if db_ok:
            ## product_in_db = self.db_interactions.check_product_in_db(product_ref)
        #     product_in_db = Product.objects.filter(ref=product_info["ref"]).exists()
        #     if not product_in_db:
        #         product_info = self.get_selected_product(product_ref)
        #         self.db_interactions._set_product_for_user_registration(product_info)
            ## self.db_interactions.save_product_for_user(username, product_ref)
        #     user = User.objects.get(username=username)
        #     product = Product.objects.get(ref=product_info["ref"])
        #     user.profile.products.add(product.id)
        
        #     status = "registered"
        # else:
        #     status = "database full"

        # return status