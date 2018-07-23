#! /usr/bin/env python3
# coding: utf-8
from unittest.mock import patch
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Product, Category, Profile
from ..utils.db_interactions  import DBInteractions

class TestDBInteractions(TestCase):
    """
    This class groups the unit tests linked to the public methods
    from DBInteractions class
    """

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """
        The objective is to integrate some categories and products with their relations
        in order to tests the query analysis' methods on a similar environment than the production
        """

        categories = [
            {
                "products": 32107,
                "name": "Aliments et boissons à base de végétaux",
                "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
                "id": "en:plant-based-foods-and-beverages"
            },
            {
                "id": "en:plant-based-foods",
                "url": "https://fr.openfoodfacts.org/categorie/aliments-d-origine-vegetale",
                "products": 27435,
                "name": "Aliments d'origine végétale"
            },
            {
                "products": 21875,
                "name": "Boissons",
                "url": "https://fr.openfoodfacts.org/categorie/boissons",
                "sameAs": [
                    "https://www.wikidata.org/wiki/Q40050"
                ],
                "id": "en:beverages"
            },
            {
                "url": "https://fr.openfoodfacts.org/categorie/boissons-non-sucrees",
                "name": "Boissons non sucrées",
                "products": 9153,
                "id": "en:non-sugared-beverages"
            },
            {
                "products": 8006,
                "name": "Produits fermentés",
                "url": "https://fr.openfoodfacts.org/categorie/produits-fermentes",
                "id": "en:fermented-foods"
            },
            {
                "id": "en:fermented-milk-products",
                "sameAs": [
                    "https://www.wikidata.org/wiki/Q3506176"
                ],
                "products": 8002,
                "name": "Produits laitiers fermentés",
                "url": "https://fr.openfoodfacts.org/categorie/produits-laitiers-fermentes"
            },
            {
                "id": "en:non-alcoholic-beverages",
                "url": "https://fr.openfoodfacts.org/categorie/boissons-sans-alcool",
                "products": 7646,
                "name": "Boissons sans alcool"
            },
            {
                "url": "https://fr.openfoodfacts.org/categorie/biscuits-et-gateaux",
                "products": 7294,
                "name": "Biscuits et gâteaux",
                "id": "en:biscuits-and-cakes"
            },
            {
                "id": "en:meats",
                "products": 7191,
                "name": "Viandes",
                "url": "https://fr.openfoodfacts.org/categorie/viandes"
            },
            {
                "id": "en:spreads",
                "url": "https://fr.openfoodfacts.org/categorie/produits-a-tartiner",
                "products": 6724,
                "name": "Produits à tartiner"
            },
        ]

        products = [
            {
                "product_name_fr": "Le jus de raisin 100% jus de fruits",
                "code": "123456789",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr" : "jus de fruit naturel sans sucre ajouté",
                "categories_hierarchy": [
                    "en:plant-based-foods-and-beverages",
                    "en:beverages",
                ],
            },
            {
                "product_name_fr": "Le haricot 100% naturellement bleue",
                "code": "987654321",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "nutrition_grade_fr": "b",
                "generic_name_fr" : "",
                "categories_hierarchy": [
                    "en:plant-based-foods",
                ],
            },
            {
                "product_name_fr": "cola à la mousse de bière",
                "code": "456789123",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "d",
                "generic_name_fr" : "du coca et de la bière, ca mousse pas mal",
                "categories_hierarchy": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
                ],
            },
            {
                "product_name_fr": "Banane à la feuille de coca",
                "code": "12345787459",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "",
                "categories_hierarchy": [
                    "en:plant-based-foods-and-beverages",
                    "en:beverages",
                    "en:biscuits-and-cakes"
                ],
            },
            {
                "product_name_fr": "steack charal",
                "code": "987695121",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "generic_name_fr":"mmmmmmhhhh Charal!!",
                "nutrition_grade_fr": "a",
                "categories_hierarchy": [
                    "en:meats",
                ],
            },
            {
                "product_name_fr": "nutella plein d'huiles de palme",
                "code": "4567859631223",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "pas bon pour les singes et les artères",
                "categories_hierarchy": [
                    "en:spreads",
                ],
            },
            {
                "product_name_fr": "steack de fausses viandes",
                "code": "987751251",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "ca a le gout de viande, mais c'est pas de la viande",
                "categories_hierarchy": [
                    "en:meats",
                ],
            },
            {
                "product_name_fr": "lait demi-écrémé pour une meilleure digestion",
                "code": "474369523",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "lait de vache frais",
                "categories_hierarchy": [
                    "en:non-alcoholic-beverages",
                    "en:fermented-milk-products"
                ],
            },
        ]

        for category in categories:
            Category.objects.create(name=category["name"].lower(),
                                    api_id=category["id"].lower(),
                                    total_products=category["products"],
                                    enough_good_nutriscore=True)

        for product in products:
            new_product = Product.objects.create(name=product["product_name_fr"].lower(),
                                   ref=product["code"],
                                   nutriscore=product["nutrition_grade_fr"],
                                   picture=product["image_url"],
                                   description=product["generic_name_fr"])
            
            for category in product["categories_hierarchy"]:
                try:
                    cat_in_db = Category.objects.get(api_id=category) 
                    new_product.categories.add(cat_in_db)
                except:
                    pass

        # We create a first user which registered one product
        username = 'test-ref'
        mail = 'test-ref@register.com'
        password = 'ref-test-view'
        password_check = 'ref-test-view'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="123456789")
        user_profile.products.add(product.id)

        
            
    def setUp(self):
        """
        This method just creates a QueryAnalysis object for all the tests
        """

        self.analysis = DBInteractions()

    ## PUBLIC METHODS ##

    def test_get_search_selection_category_success(self):
        """
        This tests checked all the process of queryanalysis with category found
        """
        query = "boissons gazeuses"
        result = {
                'type' : 'category',
                'number' : 4,
                'elements': [
                    {
                        'name' : 'aliments et boissons à base de végétaux',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:plant-based-foods-and-beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons non sucrées',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:non-sugared-beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons sans alcool',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:non-alcoholic-beverages',
                        'image_url' : '' 
                    },
                ]
            }
        self.assertEqual(self.analysis.get_search_selection(query), result)
    
    def test_get_search_selection_product_success(self):
        """
        This tests checked all the process of queryanalysis with category found
        """
        query = "coca cola"
        result = {
                'type' : 'product',
                'number' : 2,
                'elements': [
                    {
                        'name' : 'cola à la mousse de bière',
                        'ref' : '456789123',
                        'nutriscore' : 'd',
                        'description' : 'du coca et de la bière, ca mousse pas mal',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg' 
                    },
                    {
                        'name' : 'banane à la feuille de coca',
                        'ref' : '12345787459',
                        'nutriscore' : 'a',
                        'description' : '',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                    },
                ]
            }
        self.assertEqual(self.analysis.get_search_selection(query), result)
    
    def test_get_search_selection_fail(self):
        """
        This tests checked all the process of queryanalysis with any category foun
        """
        query = "céréales"
        result = None
        self.assertEqual(self.analysis.get_search_selection(query), result)

    def test_get_sustitute_products_in_db_category_search(self):
        element_type = "category"
        info_id = "en:beverages"
        result = {
                'type' : 'product',
                'number' : 2,
                'elements': [
                    {
                        'name' : 'le jus de raisin 100% jus de fruits',
                        'ref' : '123456789',
                        'nutriscore' : 'a',
                        'description' : 'jus de fruit naturel sans sucre ajouté',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                    },
                    {
                        'name' : 'banane à la feuille de coca',
                        'ref' : '12345787459',
                        'nutriscore' : 'a',
                        'description' : '',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                    },
                ]
            }
        self.assertEqual(self.analysis.get_substitute_products_in_db(element_type, info_id), result)
    
    def test_get_sustitute_products_in_db_product_search(self):

        element_type = "product"
        info_id = "456789123"
        result = {
            'type' : 'product',
            'number' : 2,
            'elements': [
                {
                    'name' : 'le jus de raisin 100% jus de fruits',
                    'ref' : '123456789',
                    'nutriscore' : 'a',
                    'description' : 'jus de fruit naturel sans sucre ajouté',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'name' : 'banane à la feuille de coca',
                    'ref' : '12345787459',
                    'nutriscore' : 'a',
                    'description' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
            ]
        }
        self.assertEqual(self.analysis.get_substitute_products_in_db(element_type, info_id), result)

    def test_set_register_existing_product_to_user(self):
        """
        This method tests the public method set_register_product_to_user with
        a product already existing in the database (Product table)
        """

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product = {
            "name" : "cola à la mousse de bière",
            "ref" : "456789123",
            "description": "du coca et de la bière, ca mousse pas mal",
            "nutriscore": "d",
            "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
            "categories": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
            ],
            "ingredients": "du haricot bleue mais 100% naturel.",
            "nutriments": {
                "fat": 50.1,
                "saturated_fat": 45.2,
                "sugar": 20,
                "salt": 5
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
        }

        status = self.analysis.set_register_product_to_user(user.username, product)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: cola à la mousse de bière>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

    def test_set_register_non_existing_product_to_user(self):
        """
        This method tests the public method set_register_product_to_user with
        a product which does not exist in the database (Product table)
        """
        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product = {
            "name" : "biscuits aux graines de tournesol et de sesame",
            "ref" : "99999999999",
            "description": "Un biscuit sain pour un corps sain qui aime les graines",
            "nutriscore": "a",
            "image_url": "https://static.openfoodfacts.org/images/products/152/sushine-cookie.jpg",
            "categories": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
            ],
            "ingredients": "pleins pleins de graines",
            "nutriments": {
                "fat": 0.2,
                "saturated_fat": 0.1,
                "sugar": 15,
                "salt": 3
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-ingredients.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-nutriments.jpg",
        }

        status = self.analysis.set_register_product_to_user(user.username, product)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

    @patch('search.utils.db_interactions.DBInteractions._count_global_rows_in_db')
    def test_set_register_non_existing_product_to_user_too_much_rows(self, mock_count_global_rows):
        """
        This method tests the public method set_register_product_to_user with
        a product which does not exist in the database (Product table) + different limits:
            -> a total of row to important -> product delete operations needed
        """
        
        mock_count_global_rows.return_value = 10000

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')

        product_to_delete = Product.objects.get(name='steack de fausses viandes')
        product_to_delete.last_interaction = datetime.today() - timedelta(days=2)
        product_to_delete.save()

        product = {
            "name" : "biscuits aux graines de tournesol et de sesame",
            "ref" : "99999999999",
            "description": "Un biscuit sain pour un corps sain qui aime les graines",
            "nutriscore": "a",
            "image_url": "https://static.openfoodfacts.org/images/products/152/sushine-cookie.jpg",
            "categories": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
            ],
            "ingredients": "pleins pleins de graines",
            "nutriments": {
                "fat": 0.2,
                "saturated_fat": 0.1,
                "sugar": 15,
                "salt": 3
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-ingredients.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-nutriments.jpg",
        }

        status = self.analysis.set_register_product_to_user(user.username, product)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

        product_deleted = Product.objects.filter(name='steack de fausses viandes').exists()
        self.assertEqual(product_deleted, False)

    @patch('search.utils.db_interactions.DBInteractions._count_global_rows_in_db')
    def test_set_register_non_existing_product_to_user_too_much_rows_other(self, mock_count_global_rows):
        """
        This method tests the public method set_register_product_to_user with
        a product which does not exist in the database (Product table) + different limits:
            -> a total of row to important -> product delete operations needed
            -> the product with the oldest last_interaction is registered by a user
        """
        
        mock_count_global_rows.return_value = 10000

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')

        product_to_delete = Product.objects.get(name='steack de fausses viandes')
        product_to_delete.last_interaction = datetime.today() - timedelta(days=2)
        product_to_delete.save()
        product_not_to_delete = Product.objects.get(name='le jus de raisin 100% jus de fruits')
        product_not_to_delete.last_interaction = datetime.today() - timedelta(days=4)
        product_not_to_delete.save()

        product = {
            "name" : "biscuits aux graines de tournesol et de sesame",
            "ref" : "99999999999",
            "description": "Un biscuit sain pour un corps sain qui aime les graines",
            "nutriscore": "a",
            "image_url": "https://static.openfoodfacts.org/images/products/152/sushine-cookie.jpg",
            "categories": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
            ],
            "ingredients": "pleins pleins de graines",
            "nutriments": {
                "fat": 0.2,
                "saturated_fat": 0.1,
                "sugar": 15,
                "salt": 3
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-ingredients.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-nutriments.jpg",
        }

        status = self.analysis.set_register_product_to_user(user.username, product)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

        product_deleted = Product.objects.filter(name='steack de fausses viandes').exists()
        self.assertEqual(product_deleted, False)

    @patch('search.utils.db_interactions.DBInteractions._count_global_rows_in_db')
    def test_set_register_non_existing_product_impossible_to_register(self, mock_count_global_rows):
        """
        This method tests the public method set_register_product_to_user with
        a product which does not exist in the database (Product table) + different limits:
            -> a total of row to important -> product delete operations needed
            -> all the products in the database had been registered by a user
        """

        mock_count_global_rows.return_value = 10000

        # We add a new user which register all the products from the database
        username = 'test-all-products'
        mail = 'test-products@register.com'
        password = 'products-test-full'
        password_check = 'products-test-full'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        
        for product in Product.objects.all():
            user_profile.products.add(product.id)

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        
        product = {
            "name" : "biscuits aux graines de tournesol et de sesame",
            "ref" : "99999999999",
            "description": "Un biscuit sain pour un corps sain qui aime les graines",
            "nutriscore": "a",
            "image_url": "https://static.openfoodfacts.org/images/products/152/sushine-cookie.jpg",
            "categories": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
            ],
            "ingredients": "pleins pleins de graines",
            "nutriments": {
                "fat": 0.2,
                "saturated_fat": 0.1,
                "sugar": 15,
                "salt": 3
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-ingredients.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/152/sunshine-nutriments.jpg",
        }

        status = self.analysis.set_register_product_to_user(user.username, product)
        query = user.profile.products.all()

        result = [
            "<Product: le jus de raisin 100% jus de fruits>",]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'database full') 

    ## PRIVATE METHODS ##

    def test_get_in_category_model_success(self):
        """
        This test verifies if the method get_info_in_db for Category model gets all the categories
        which own a word in the query
        """

        query = "boissons gazeuses"
        results = [
            "<Category: aliments et boissons à base de végétaux>",
            "<Category: boissons>",
            "<Category: boissons non sucrées>",
            "<Category: boissons sans alcool>"]

        self.assertQuerysetEqual(self.analysis._get_info_in_db(Category, query), results, ordered=False)

    def test_get_in_category_model_fail(self):
        """
        This tests verifies if the method get_info_in_db for Category model returns None 
        when any categories match with one word of the query
        """

        query = "nutella"
        self.assertEqual(self.analysis._get_info_in_db(Category, query), None)

    def test_get_in_product_model_success(self):
        """
        This test verifies if the method get_info_in_db for Product model gets all the products
        which own a word in the query
        """

        query = "coca cola"
        results = [
            "<Product: cola à la mousse de bière>",
            "<Product: banane à la feuille de coca>"]
        self.assertQuerysetEqual(self.analysis._get_info_in_db(Product, query), results, ordered=False)

    def test_get_in_product_model_fail(self):
        """
        This tests verifies if the method get_info_in_db for Product model returns None 
        when any products match with one word of the query
        """

        query = "céréales"
        self.assertEqual(self.analysis._get_info_in_db(Product, query), None)

    def test_queryset_to_dict_category(self):
        """
        This test checks if the method queryset_to_dict returns an appropriate dict for a categories queryset.
        It uses the get_info_in_db method to get the adequate queryset to test (same as the test before)
        """
        query = "boissons gazeuses"
        queryset = self.analysis._get_info_in_db(Category, query)
        result = {
                'type' : 'category',
                'number' : 4,
                'elements': [
                    {
                        'name' : 'aliments et boissons à base de végétaux',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:plant-based-foods-and-beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons non sucrées',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:non-sugared-beverages',
                        'image_url' : '' 
                    },
                    {
                        'name' : 'boissons sans alcool',
                        'ref' : '',
                        'nutriscore' : '',
                        'description' : 'en:non-alcoholic-beverages',
                        'image_url' : '' 
                    },
                ]
            }

        self.assertEqual(self.analysis._queryset_to_dict(queryset, "category"), result)

    def test_queryset_to_dict_product(self):
        """
        This test checks if the method queryset_to_dict returns an appropriate dict for a products queryset.
        It uses the get_info_in_db method to get the adequate queryset to test (same as the test before)
        """
        query = "coca cola"
        queryset = self.analysis._get_info_in_db(Product, query)

        result = {
                'type' : 'product',
                'number' : 2,
                'elements': [
                    {
                        'name' : 'cola à la mousse de bière',
                        'ref' : '456789123',
                        'nutriscore' : 'd',
                        'description' : 'du coca et de la bière, ca mousse pas mal',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg' 
                    },
                    {
                        'name' : 'banane à la feuille de coca',
                        'ref' : '12345787459',
                        'nutriscore' : 'a',
                        'description' : '',
                        'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                    },
                ]
            }
        self.assertEqual(self.analysis._queryset_to_dict(queryset, "product"), result)

    def test_count_global_rows_in_db(self):
        print(self.analysis._count_global_rows_in_db())
        self.assertEqual(self.analysis._count_global_rows_in_db(), 33)