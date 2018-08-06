#! /usr/bin/env python3
# coding: utf-8
from unittest.mock import patch
from django.test import TestCase
from ..management.commands.dbinit import DBInit
from django.contrib.auth.models import User
from..models import Product, Category, Profile

class TestCommandDBInit(TestCase):
    """
    This class groups the unit tests linked to the public methods from
    the DBInit class (command to initialize the database for the beta app [< 10k rows])
    """

    maxDiff= None

    @classmethod
    def setUpTestData(cls):
        """
        The objective is to integrate some categories and products with their relations
        in order to tests the query analysis' methods on a similar environment than the production
        """

        categories = [
            {
                "products": 950,
                "name": "Nourritures magiques",
                "url": "https://fr.openfoodfacts.org/categorie/nourritures-magiques",
                "id": "en:magic-foods"
            },
            {
                "id": "en:cereales",
                "url": "https://fr.openfoodfacts.org/categorie/cereales",
                "products": 150,
                "name": "grains"
            },
            {
                "products": 500,
                "name": "oiseaux",
                "url": "https://fr.openfoodfacts.org/categorie/oiseaux",
                "sameAs": [
                    "https://www.wikidata.org/wiki/Q40050"
                ],
                "id": "en:birds"
            },
            {
                "url": "https://fr.openfoodfacts.org/categorie/insects",
                "name": "insectes",
                "products": 750,
                "id": "en:insects"
            },
        ]

        products = [
            {
                "product_name_fr": "haricots magiques",
                "code": "9",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr" : "haricot qui fait grandir",
                "categories_hierarchy": [
                    "en:magic-food",
                    "en:what-the-fuck",
                ],
            },
            {
                "product_name_fr": "perroquet",
                "code": "987",
                "image_url": "https://static.openfoodfacts.org/images/products/152/perroquet.jpg",
                "nutrition_grade_fr": "d",
                "generic_name_fr" : "",
                "categories_hierarchy": [
                    "en:birds",
                ],
            },
            {
                "product_name_fr": "muesli au chocolat",
                "code": "456",
                "image_url": "https://static.openfoodfacts.org/images/products/152/muesli.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr" : "enfin un truc qui se mange",
                "categories_hierarchy": [
                    "en:cereales",
                    "en:plant-based-foods-and-beverages",
                ],
            },
            {
                "product_name_fr": "criquets",
                "code": "59",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.99.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "on prend si vraiment on a faim",
                "categories_hierarchy": [
                    "en:insects",
                    "en:beverages",
                    "en:biscuits-and-cakes"
                ],
            },
            {
                "product_name_fr": "poissons fées",
                "code": "987691",
                "image_url": "https://static.openfoodfacts.org/images/products/152/poissons.jpg",
                "generic_name_fr":"ca vole",
                "nutrition_grade_fr": "d",
                "categories_hierarchy": [
                    "en:magic-foods",
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

        # We create some users
        
        #First one
        username = 'test-ref'
        mail = 'test-ref@register.com'
        password = 'ref-test-view'
        password_check = 'ref-test-view'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="9")
        user_profile.products.add(product.id)
        product = Product.objects.get(ref="987")
        user_profile.products.add(product.id)

        #Second one
        username = 'test-update'
        mail = 'test-update@dbinit.com'
        password = 'ref-update'
        password_check = 'ref-update'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="59")
        user_profile.products.add(product.id)
        product = Product.objects.get(ref="987691")
        user_profile.products.add(product.id)

    def setUp(self):
        self.db_init = DBInit()

        self.categories_api_return = {
            "count" : 13936,           
            "tags" : [
                {
                    "products": 30000,
                    "name": "Aliments et boissons à base de végétaux",
                    "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
                    "id": "en:plant-based-foods-and-beverages"
                },
                {
                    "id": "en:cereales",
                    "url": "https://fr.openfoodfacts.org/categorie/cereales",
                    "products": 150,
                    "name": "grains"
                },
                {
                    "id": "en:magic-beverages",
                    "url": "https://fr.openfoodfacts.org/categorie/boissons-magiques",
                    "products": 850,
                    "name": "Boissons magiques"
                },
                {
                    "products": 50,
                    "name": "Biscuits de druides",
                    "url": "https://fr.openfoodfacts.org/categorie/biscuits-de-druides",
                    "sameAs": [
                        "https://www.wikidata.org/wiki/Q40050"
                    ],
                    "id": "en:druids-cookies"
                },
            ]
        }

        self.products_api_return = {
            "skip" : 0,
            "page" : 1,
            "page_size" : 1000,
            "count" : 9,
            "products" : [
                {
                    "product_name_fr": "potion magique de santé",
                    "code": "951753",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/sante.jpg",
                    "generic_name_fr":"ca requinque la life",
                    "nutrition_grade_fr": "a",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de bave de crapaud",
                    "code": "49123",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/degueu.jpg",
                    "nutrition_grade_fr": "d",
                    "generic_name_fr": "degueu",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de nutella",
                    "code": "9877",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/nutella-degueu.jpg",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "encore plus mauvais que l'original",
                    "categories_hierarchy": [
                        "en:meats",
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion musclor",
                    "code": "47",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/musclor.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ahouuuuuuuuuu",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                        "em:meat-ultra",
                    ],
                },
                                {
                    "product_name_fr": "potion de bouse",
                    "code": "7",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/bouse.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "hhhmmmmm c'est delicieux",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de grand mère",
                    "code": "52894631",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/old.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "périmé",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "jus de chaussettes",
                    "code": "4749763",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/shoes.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "pas fou en gout mais ca requinque",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "liquide inconnu",
                    "code": "9523",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/unknown.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ca se teste",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "jus de prune",
                    "code": "47433",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/prune.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ca lave",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
            ]
        }

    def test_clean_db_without_data(self):
        """
        This method tests if the method deletes all the data from the database
        """

        self.db_init.clean_db()

        query = Category.objects.all().exists()
        self.assertEqual(query, False)

        query = Product.objects.all().exists()
        self.assertEqual(query, False)

        query = User.objects.all().exists()
        self.assertEqual(query, False)

        query = Profile.objects.all().exists()
        self.assertEqual(query, False)


    @patch('search.management.commands.dbinit.DBInit._get_from_api_products_info_from_page_category')
    @patch('search.management.commands.dbinit.DBInit._get_categories_from_api')
    def test_db_create(self, mock_get_categories_from_api, mock_api_product):
        """
        The idea is to test if the database is cleaned with news datas when we want to recreate the database
        """

        # config of mock return value
        mock_get_categories_from_api.return_value = self.categories_api_return
        mock_api_product.return_value = self.products_api_return

        # operation from dbinit --create commands
        self.db_init.clean_db()
        self.db_init.set_categories()
        self.db_init.set_products()

        # tests
        category_number = Category.objects.all().count()
        self.assertEqual(category_number, 1)

        product_number = Product.objects.all().count()
        self.assertEqual(product_number, 8)

        users = User.objects.all().exists()
        self.assertEqual(users, False)

        profiles = Profile.objects.all().exists()
        self.assertEqual(profiles, False)

        categories = Category.objects.all()
        categories_result = [
            "<Category: boissons magiques>",
        ]
        self.assertQuerysetEqual(categories, categories_result, ordered=False)

        products = Product.objects.all()
        products_result = [
            "<Product: potion magique de sante>",
            "<Product: potion de bave de crapaud>",
            "<Product: potion de nutella>",
            "<Product: potion musclor>",
            "<Product: potion de bouse>",
            "<Product: potion de grand mere>",
            "<Product: jus de chaussettes>",
            "<Product: liquide inconnu>",
        ]
        self.assertQuerysetEqual(products, products_result, ordered=False)

    @patch('search.management.commands.dbinit.DBInit._get_from_api_products_info_from_page_category')
    @patch('search.management.commands.dbinit.DBInit._get_categories_from_api')
    def test_db_update(self, mock_get_categories_from_api, mock_api_product):
        """
        The objective is to test if the update works when there are some datas in the database
        """
        # config of mock return value
        mock_get_categories_from_api.return_value = self.categories_api_return
        mock_api_product.return_value = self.products_api_return

        # operation from dbinit --create commands
        self.db_init.set_categories()
        self.db_init.set_products()

        # tests
        users = User.objects.all().exists()
        self.assertEqual(users, True)

        user_number = User.objects.all().count()
        self.assertEqual(user_number, 2)

        users = User.objects.all()
        users_result = [
            "<User: test-ref>",
            "<User: test-update>",
        ]
        self.assertQuerysetEqual(users, users_result, ordered=False)

        profiles = Profile.objects.all().exists()
        self.assertEqual(profiles, True)

        profile_number = Profile.objects.all().count()
        self.assertEqual(profile_number, 2)

        user = User.objects.get(username='test-ref')
        user_product_numb = user.profile.products.all().count()
        self.assertEqual(user_product_numb, 2)

        user_products = user.profile.products.all()
        user_products_result = [
            "<Product: haricots magiques>",
            "<Product: perroquet>",
        ]
        self.assertQuerysetEqual(user_products, user_products_result, ordered=False)

        user = User.objects.get(username='test-update')
        user_product_numb = user.profile.products.all().count()
        self.assertEqual(user_product_numb, 2)

        user_products = user.profile.products.all()
        user_products_result = [
            "<Product: criquets>",
            "<Product: poissons fées>",
        ]
        self.assertQuerysetEqual(user_products, user_products_result, ordered=False)

        category_number = Category.objects.all().count()
        self.assertEqual(category_number, 5)

        product_number = Product.objects.all().count()
        self.assertEqual(product_number, 13)

        categories = Category.objects.all()
        categories_result = [
            "<Category: boissons magiques>",
            "<Category: nourritures magiques>",
            "<Category: grains>",
            "<Category: oiseaux>",
            "<Category: insectes>",
        ]
        self.assertQuerysetEqual(categories, categories_result, ordered=False)

        products = Product.objects.all()
        products_result = [
            "<Product: haricots magiques>",
            "<Product: perroquet>",
            "<Product: muesli au chocolat>",
            "<Product: criquets>",
            "<Product: poissons fées>",
            "<Product: potion magique de sante>",
            "<Product: potion de bave de crapaud>",
            "<Product: potion de nutella>",
            "<Product: potion musclor>",
            "<Product: potion de bouse>",
            "<Product: potion de grand mere>",
            "<Product: jus de chaussettes>",
            "<Product: liquide inconnu>",
        ]
        self.assertQuerysetEqual(products, products_result, ordered=False)