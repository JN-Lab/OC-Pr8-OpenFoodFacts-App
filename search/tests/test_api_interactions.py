#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from unittest.mock import patch
from search.utils.api_interactions import OpenFoodFactsInteractions

class TestApiInteractions(TestCase):
    """
    This class groups all the unit tests linked to the public methods
    from OpenFoodFactsInteractions class
    """

    maxDiff = None

    def setUp(self):

        self.api_interaction = OpenFoodFactsInteractions()

        self.data_received = {
            "count" : 18,
            "products": [
                {
                    "product_name_fr" : "Nutella",
                    "code": "3017620429484",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Cre Avela Nute",
                    "code": "38562429484",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "on sait pas mais c'est grec",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Pâte à Tartiner Nutella,",
                    "code": "364561612564",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Pate Tartiner Nutella 750G",
                    "code": "54651861",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Biscuits nutella",
                    "code": "3855648164",
                    "nutrition_grade_fr": "",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "B-ready",
                    "code": "38455162",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Biscuits B Ready noisettes/cacao Nutella",
                    "code": "3453548914",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "code": "385657387484",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Nutella au caramel",
                    "code": "301776542",
                    "nutrition_grade_fr": "b",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au caramel",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Jambon au cacao",
                    "code": "385647458574524",
                    "nutrition_grade_fr": "",
                    "generic_name_fr": "on sait pas mais c'est grec",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "gateaux Nutella et caramel,",
                    "code": "364561614754",
                    "nutrition_grade_fr": "b",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Nutella light",
                    "code": "54651861",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "nute et la",
                    "code": "3855647475284",
                    "nutrition_grade_fr": "",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "B-not-ready",
                    "code": "384551677252",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Biscuits granola",
                    "code": "34535489",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
                    "product_name_fr" : "Nutella in da mix",
                    "code": "385657387484",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "",
                    "image_url": "",
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
                    "product_name_fr" : "Nutella c'est bon",
                    "code": "3856573872569",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "pour tester l'absence de categories_hierarchy",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "product_name_fr" : "Nutella c'est pas bon pour la santé",
                    "code": "385657395169",
                    "nutrition_grade_fr": "d",
                    "generic_name_fr": "pour tester l'absence de categories_hierarchy",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
            ]
        }

        self.selected_products = {
            'type' : 'product',
            'number' : 9,
            'elements' : [
                {
                    "name" : "Nutella",
                    "ref": "3017620429484",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Pâte à Tartiner Nutella,",
                    "ref": "364561612564",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Pate Tartiner Nutella 750G",
                    "ref": "54651861",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Biscuits B Ready noisettes/cacao Nutella",
                    "ref": "3453548914",
                    "nutriscore": "e",
                    "description": "",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Nutella",
                    "ref": "385657387484",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },  
                {
                    "name" : "Nutella au caramel",
                    "ref": "301776542",
                    "nutriscore": "b",
                    "description": "Pâtes à tartiner aux noisettes et au caramel",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "gateaux Nutella et caramel,",
                    "ref": "364561614754",
                    "nutriscore": "b",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_search')
    def test_get_products_selection(self, mock_get_products_from_api):

        mock_get_products_from_api.return_value = self.data_received
        result = {
            'type' : 'product',
            'number' : 6,
            'elements' : [
                {
                    "name" : "Nutella",
                    "ref": "3017620429484",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Pâte à Tartiner Nutella,",
                    "ref": "364561612564",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Pate Tartiner Nutella 750G",
                    "ref": "54651861",
                    "nutriscore": "e",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "Biscuits B Ready noisettes/cacao Nutella",
                    "ref": "3453548914",
                    "nutriscore": "e",
                    "description": "",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                }, 
                {
                    "name" : "Nutella au caramel",
                    "ref": "301776542",
                    "nutriscore": "b",
                    "description": "Pâtes à tartiner aux noisettes et au caramel",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "gateaux Nutella et caramel,",
                    "ref": "364561614754",
                    "nutriscore": "b",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
            ] 
        }

        self.assertEqual(self.api_interaction.get_products_selection("nutella", 6), result)
    
    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_search')
    def test_get_substitute_products_from_api_category_search_success(self, mock_get_products_from_api):
        mock_get_products_from_api.return_value = self.data_received
        result =   {
            'type' : 'product',
            'number' : 4,
            'elements' : [
                {
                    "name" : "Nutella light",
                    "ref": "54651861",
                    "nutriscore": "a",
                    "description": "Pâtes à tartiner aux noisettes et au cacao",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
                {
                    "name" : "B-not-ready",
                    "ref": "384551677252",
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
                },
                {
                    "name" : "Nutella c'est bon",
                    "ref": "3856573872569",
                    "nutriscore": "a",
                    "description": "pour tester l'absence de categories_hierarchy",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                },
            ]
        }
        self.assertEqual(self.api_interaction.get_substitute_products_from_api("category", "en:beverages", 6), result)
    
    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_search')
    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_product_from_api_code_search')
    def test_get_substitute_products_from_api_product_search_fail(self, mock_api_code, mock_api_category):
        
        code = "3017620429484"
        mock_api_code.return_value = {
            "status": 1,
            "status_verbose": "product found",
            "product": {
                "product_name_fr" : "Nutella",
                "code": "3017620429484",
                "nutrition_grade_fr": "e",
                "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
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
        }
        mock_api_category.return_value = self.data_received

        self.assertEqual(self.api_interaction.get_substitute_products_from_api("product", code, 6), None)

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_product_from_api_code_search')
    def test_get_selected_product_success(self, mock_api_code):

        code = "3017620429484"
        mock_api_code.return_value = {
            "status": 1,
            "status_verbose": "product found",
            "code": "3017620429484",
            "product": {
                "product_name_fr" : "Nutella",
                "code": "3017620429484",
                "nutrition_grade_fr": "e",
                "generic_name_fr": "Pâtes à tartiner aux noisettes et au cacao",
                "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
                "categories_hierarchy": [
                    "en:breakfasts",
                    "en:spreads",
                    "en:sweet-spreads",
                    "fr:pates-a-tartiner",
                    "en:chocolate-spreads",
                    "en:hazelnut-spreads",
                    "en:cocoa-and-hazelnuts-spreads"
                ],
                "nutriments": {
                    "nutrition-score-fr": "26",
                    "sugars_100g": 56.3,
                    "fat_100g": 30.9,
                    "salt": 0.1,
                    "saturated-fat_100g": 10.6,
                    "salt_100g": 0.1,
                    "salt_value": "0.1",
                },
                "ingredients_text_fr": "Sucre, huile de palme, _noisettes_ 13 %, cacao maigre 7,4 %, _lait_ écrémé en poudre 6,6 %, _lactosérum_ en poudre, émulsifiants : lécithines (_soja_), vanilline.",
                "image_nutrition_url": "https://static.openfoodfacts.org/images/products/301/762/042/9484/nutrition_fr.106.400.jpg",
                "image_ingredients_url": "https://static.openfoodfacts.org/images/products/301/762/042/9484/ingredients_fr.149.400.jpg",                               
            },
        }

        result = {
            "name" : "Nutella",
            "ref" : "3017620429484",
            "description": "Pâtes à tartiner aux noisettes et au cacao",
            "nutriscore": "e",
            "image_url": "https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.400.jpg",
            "categories": [
                    "en:breakfasts",
                    "en:spreads",
                    "en:sweet-spreads",
                    "fr:pates-a-tartiner",
                    "en:chocolate-spreads",
                    "en:hazelnut-spreads",
                    "en:cocoa-and-hazelnuts-spreads"
                ],
            "ingredients": "Sucre, huile de palme, _noisettes_ 13 %, cacao maigre 7,4 %, _lait_ écrémé en poudre 6,6 %, _lactosérum_ en poudre, émulsifiants : lécithines (_soja_), vanilline.",
            "nutriments": {
                "fat": 30.9,
                "saturated_fat": 10.6,
                "sugar": 56.3,
                "salt": 0.1
            },
            "ingredients_image_url": "https://static.openfoodfacts.org/images/products/301/762/042/9484/ingredients_fr.149.400.jpg",
            "nutriments_image_url": "https://static.openfoodfacts.org/images/products/301/762/042/9484/nutrition_fr.106.400.jpg",    
        }
        self.assertEqual(self.api_interaction.get_selected_product(code), result)

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_product_from_api_code_search')
    def test_get_selected_product_fail(self, mock_api_code):

        code = "3017620429484"
        mock_api_code.return_value = {
            "status": 1,
            "status_verbose": "product found",
            "code": "3017620429484",
            "product": {
                "product_name_fr" : "Nutella",
                "code": "3017620429484",
                "nutrition_grade_fr": "e",
                "generic_name_fr": "",
                "nutriments": {
                    "nutrition-score-fr": "26",
                    "salt": 0.1,
                    "saturated-fat_100g": 10.6,
                    "salt_value": "0.1",
                },
                "image_nutrition_url": "",
            },
        }

        result = {
            "name" : "Nutella",
            "ref" : "3017620429484",
            "description": "Information manquante",
            "nutriscore": "e",
            "image_url": "Image manquante",
            "categories": [
                    "Information manquante"
                ],
            "ingredients": "Information manquante",
            "nutriments": {
                "fat": -1,
                "saturated_fat": 10.6,
                "sugar": -1,
                "salt": -1
            },
            "ingredients_image_url": "Image manquante",
            "nutriments_image_url": "Image manquante",    
        }
        self.assertEqual(self.api_interaction.get_selected_product(code), result)