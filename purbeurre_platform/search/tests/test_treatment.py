#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from unittest.mock import patch
from search.utils.query_analysis import QueryAnalysis
from search.utils.api_interactions import OpenFoodFactsInteractions
from search.utils.treatment import Treatment

class TestTreatment(TestCase):

    maxDiff = None

    @patch('search.utils.api_interactions.OpenFoodFactsInteractions._get_products_from_api')
    @patch('search.utils.query_analysis.QueryAnalysis.get_search_selection')
    def test_get_choice_selection_api_success(self, mock_get_search_selection, mock_get_products_from_api):
        api_response = {
            "skip": 0,
            "page": 1,
            "page_size": "150",
            "count": 11,
            "products": [
                {
                    "product_name_fr" : "Nutella",
                    "nutrition_grade_fr" : "d",
                    "code" : "456789123",
                    "generic_name_fr" : "le vrai et l'unique",
                    "image_url" : "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                },
                {
                    'product_name_fr' : 'glace au nutella',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'c',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'a',
                    'generic_name_fr' : 'un produit sans nom',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'product_name_fr' : 'nutella à la banane et noix de coco',
                    'code' : '12345787459',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                                {
                    "product_name_fr" : "Nutella",
                    "nutrition_grade_fr" : "d",
                    "code" : "456789953",
                    "generic_name_fr" : "le vrai et l'unique une nouvelle fois",
                    "image_url" : "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                },
                {
                    'product_name_fr' : 'glace au nutella light',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'a',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'product_name_fr' : 'nutella et chantilly dans le pot',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'c',
                    'generic_name_fr' : "c'est gras mais c'est bon",
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'product_name_fr' : 'nutella avec de la banane et sa peau',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'b',
                    'generic_name_fr' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
                {
                    'product_name_fr' : 'nutella bio',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'b',
                    'generic_name_fr' : 'la blague!',
                },
                {
                    'product_name_fr' : 'nutella sans huile mais avec de la graisse de porc',
                    'code' : '4796563787459',
                    'nutrition_grade_fr' : 'd',
                    'generic_name_fr' : '',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg'
                },
                {
                    'product_name_fr' : 'nutella en biscuit',
                    'code' : '12345787459',
                    'nutrition_grade_fr' : 'd',
                    'generic_name_fr' : 'une description mais pas très utile',
                    'image_url' : 'https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg' 
                },
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

        treatment = Treatment()
        self.assertEqual(treatment.get_choice_selection("nutella"), result)

    def test_get_choice_selection_db_success(self):
        pass