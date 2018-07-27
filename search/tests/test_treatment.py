#! /usr/bin/env python3
# coding: utf-8
from datetime import datetime, timedelta
from django.test import TestCase
from unittest.mock import patch
from search.utils.db_interactions import DBInteractions
from search.utils.api_interactions import OpenFoodFactsInteractions
from search.utils.treatment import Treatment
from django.contrib.auth.models import User
from ..models import Product, Category, Profile

class TestTreatment(TestCase):
    """
    This class groups the unit tests linked to the Treatment class
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
        self.treatment = Treatment()

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_search')
    @patch('search.utils.db_interactions.DBInteractions.get_search_selection')
    def test_get_choice_selection_api_success(self, mock_get_search_selection, mock_get_products_from_api):
        api_response = {
            "skip": 0,
            "page": 1,
            "page_size": "150",
            "count": 13,
            "products": [
                {
                    "product_name_fr" : "Nutella",
                    "nutrition_grade_fr" : "d",
                    "code" : "456789123",
                    "generic_name_fr" : "le vrai et l'unique",
                    "image_url" : "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'product_name_fr' : 'glace au nutella',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'c',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'a',
                    'generic_name_fr' : 'un produit sans nom',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'product_name_fr' : 'nutella à la banane et noix de coco',
                    'code' : '12345787459',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ], 
                },
                {
                    "product_name_fr" : "Nutella",
                    "nutrition_grade_fr" : "d",
                    "code" : "456789953",
                    "generic_name_fr" : "le vrai et l'unique une nouvelle fois",
                    "image_url" : "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'product_name_fr' : 'glace au nutella light',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'a',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ], 
                },
                {
                    'product_name_fr' : 'nutella et chantilly dans le pot',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'c',
                    'generic_name_fr' : "c'est gras mais c'est bon",
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ], 
                },
                {
                    'product_name_fr' : 'nutella avec de la banane et sa peau',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'b',
                    'generic_name_fr' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ], 
                },
                {
                    'product_name_fr' : 'nutella bio',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'b',
                    'generic_name_fr' : 'la blague!',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'product_name_fr' : 'nutella sans huile mais avec de la graisse de porc',
                    'code' : '4796563787459',
                    'nutrition_grade_fr' : 'd',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ],
                },
                {
                    'product_name_fr' : 'nutella en biscuit',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'd',
                    'generic_name_fr' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg',
                    "categories_hierarchy": [
                        "en:breakfasts",
                        "en:spreads",
                        "en:sweet-spreads",
                        "fr:pates-a-tartiner",
                        "en:chocolate-spreads",
                        "en:hazelnut-spreads",
                        "en:cocoa-and-hazelnuts-spreads"
                    ], 
                },
                {
                    "name" : "Nutella light",
                    "ref": "54651861",
                    "nutriscore": "a",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Nutella in da mix",
                    "ref": "385657387484",
                    "nutriscore": "a",
                    "description": "",
                    "image_url": "",
                }
            ]
        }

        mock_get_search_selection.return_value = None
        mock_get_products_from_api.return_value = api_response
        
        result = {
            'type' : 'product',
            'number' : 6,
            'elements': [
                {
                    'name' : 'Nutella',
                    'ref' : '456789123',
                    'nutriscore' : 'd',
                    'description' : "le vrai et l'unique",
                    'image_url' : 'https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg' 
                },
                {
                    'name' : 'glace au nutella',
                    'ref' : '12345787459',
                    'nutriscore' : 'c',
                    'description' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'name' : 'nutella et chantilly dans le pot',
                    'ref' : '12345787459',
                    'nutriscore' : 'c',
                    'description' : "c'est gras mais c'est bon",
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'name' : 'nutella avec de la banane et sa peau',
                    'ref' : '12345787459',
                    'nutriscore' : 'b',
                    'description' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'name' : 'nutella sans huile mais avec de la graisse de porc',
                    'ref' : '4796563787459',
                    'nutriscore' : 'd',
                    'description' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg'
                },
                {
                    'name' : 'nutella en biscuit',
                    'ref' : '12345787459',
                    'nutriscore' : 'd',
                    'description' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
            ]
        }

        self.assertEqual(self.treatment.get_choice_selection("nutella"), result)

    def test_register_product_existing_product_to_user(self):
        """
        This method tests the public method register_product with
        a product already existing in the database (Product table)
        """

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product_ref = "456789123" 

        status = self.treatment.register_product(user.username, product_ref)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: cola à la mousse de bière>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

    @patch('search.utils.treatment.Treatment.get_selected_product')
    def test_register_product_non_existing_product_to_user(self, mock_get_selected_product):
        """
        This method tests the public method register_product with
        a product which does not exist in the database (Product table)
        """
        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product_ref = "99999999999" 
        mock_get_selected_product.return_value = {
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

        status = self.treatment.register_product(user.username, product_ref)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

    @patch('search.utils.treatment.Treatment.get_selected_product')
    @patch('search.utils.db_interactions.DBInteractions.count_global_rows_in_db')
    def test_register_product_non_existing_product_to_user_too_much_rows(self, mock_count_global_rows, mock_get_selected_product):
        """
        This method tests the public method register_product with
        a product which does not exist in the database (Product table) + different limits:
            -> a total of row to important -> product delete operations needed
        """
        
        mock_count_global_rows.return_value = 10000

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product_ref = "99999999999"

        product_to_delete = Product.objects.get(name='steack de fausses viandes')
        product_to_delete.last_interaction = datetime.today() - timedelta(days=2)
        product_to_delete.save()

        mock_get_selected_product.return_value = {
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

        status = self.treatment.register_product(user.username, product_ref)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

        product_deleted = Product.objects.filter(name='steack de fausses viandes').exists()
        self.assertEqual(product_deleted, False)

    @patch('search.utils.treatment.Treatment.get_selected_product')
    @patch('search.utils.db_interactions.DBInteractions.count_global_rows_in_db')
    def test_register_product_non_existing_product_to_user_too_much_rows_other(self, mock_count_global_rows, mock_get_selected_product):
        """
        This method tests the public method register_product with
        a product which does not exist in the database (Product table) + different limits:
            -> a total of row to important -> product delete operations needed
            -> the product with the oldest last_interaction is registered by a user
        """
        
        mock_count_global_rows.return_value = 10000

        user = self.client.login(username='test-ref', password='ref-test-view')

        user = User.objects.get(username='test-ref')
        product_ref = "99999999999"

        product_to_delete = Product.objects.get(name='steack de fausses viandes')
        product_to_delete.last_interaction = datetime.today() - timedelta(days=2)
        product_to_delete.save()
        product_not_to_delete = Product.objects.get(name='le jus de raisin 100% jus de fruits')
        product_not_to_delete.last_interaction = datetime.today() - timedelta(days=4)
        product_not_to_delete.save()

        mock_get_selected_product.return_value = {
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

        status = self.treatment.register_product(user.username, product_ref)
        query = user.profile.products.all()
        result = [
            "<Product: le jus de raisin 100% jus de fruits>", 
            "<Product: biscuits aux graines de tournesol et de sesame>"]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'registered')

        product_deleted = Product.objects.filter(name='steack de fausses viandes').exists()
        self.assertEqual(product_deleted, False)

    @patch('search.utils.treatment.Treatment.get_selected_product')
    @patch('search.utils.db_interactions.DBInteractions.count_global_rows_in_db')
    def test_register_product_non_existing_product_impossible_to_register(self, mock_count_global_rows, mock_get_selected_product):
        """
        This method tests the public method register_product with
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
        product_ref = "99999999999"
        
        mock_get_selected_product.return_value = {
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

        status = self.treatment.register_product(user.username, product_ref)
        query = user.profile.products.all()

        result = [
            "<Product: le jus de raisin 100% jus de fruits>",]
        self.assertQuerysetEqual(query, result, ordered=False)
        self.assertEqual(status, 'database full') 