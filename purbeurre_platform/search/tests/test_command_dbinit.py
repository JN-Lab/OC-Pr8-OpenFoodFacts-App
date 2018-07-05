#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from ..management.commands.dbinit import DBInit
from..models import Product, Category

class TestCommandDBInit(TestCase):

    maxDiff= None

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
                "code": "456789123",
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

    def setUp(self):
        self.db_init = DBInit()

    def test_clean_db_without_data(self):
        result = []
        
        self.db_init.clean_db()

        query = Category.objects.all()
        self.assertQuerysetEqual(query, result)

        query = Product.objects.all()
        self.assertQuerysetEqual(query, result)

    def test_set_categories(self):
        pass
        
