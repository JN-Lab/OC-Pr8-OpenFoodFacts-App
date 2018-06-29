from django.test import TestCase
from ..models import Product, Category
from ..utils.query_analysis  import QueryAnalysis

class TestQueryAnalysis(TestCase):

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
            }
        ]

        products = [
            {
                "product_name_fr": "Le jus de raisin 100% jus de fruits",
                "code": "123456789",
                "img_thumb_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "categories_hierarchy": [
                    "en:plant-based-foods-and-beverages",
                    "en:beverages",
                ],
            },
            {
                "product_name_fr": "Le haricot 100% naturellement bleue",
                "code": "987654321",
                "img_thumb_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "nutrition_grade_fr": "b",
                "categories_hierarchy": [
                    "en:plant-based-foods",
                ],
            },
            {
                "product_name_fr": "cola à la mousse de bière",
                "code": "456789123",
                "img_thumb_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "d",
                "categories_hierarchy": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
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
                                   picture=product["img_thumb_url"])
            
            for category in product["categories_hierarchy"]:
                cat_in_db = Category.objects.get(api_id=category) 
                if cat_in_db:
                    new_product.categories.add(cat_in_db)
            
    def setUp(self):
        self.analysis = QueryAnalysis()
        self.success_query_cat = "boissons gazeuses"
        self.fail_query_cat = "nutella"
        self.success_query_product = "coca cola"
        self.fail_query_product = "céréales"

    def test_exists_in_category_success(self):
        # A modifier -> Retourner QuerySet or None
        print(Product.objects.all())
        self.assertTrue(self.analysis.exists_in_category(self.success_query_cat))