#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from unittest.mock import patch
from search.utils.api_interactions import OpenFoodFactsInteractions

class TestApiInteractions(TestCase):

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

    ## PUBLIC METHODS ##

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_brand_search')
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
    
    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_category_search')
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
    
    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api_category_search')
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


    ## PRIVATE METHODS ##

    def test_select_appropriate_products_success(self):

        self.assertEqual(self.api_interaction._select_appropriate_products(self.data_received, "nutella"), self.selected_products)

    def test_select_by_image(self):

        result = {
            'type' : 'product',
            'number' : 8,
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
            ] 
        }

        self.assertEqual(self.api_interaction._select_by_image(self.selected_products, 6), result)

    def test_select_by_description(self):

        result = {
            'type' : 'product',
            'number' : 7,
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
            ] 
        }       
        self.assertEqual(self.api_interaction._select_by_description(self.selected_products, 6), result)

    def test_select_by_nutriscore_value(self):

        result = {
            'type' : 'product',
            'number' : 7,
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
                }
            ] 
        }
        self.assertEqual(self.api_interaction._select_by_nutriscore_value(self.selected_products, 6), result)
    
    def test_select_by_product_name(self):
        
        result = {
            'type' : 'product',
            'number' : 8,
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
        self.assertEqual(self.api_interaction._select_by_product_name(self.selected_products, 6), result)