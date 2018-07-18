#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..views import index, choice
from ..utils.treatment import Treatment
from ..models import Product, Category, Profile

class IndexPageTestCase(TestCase):
    """
    This class tests the index page view
    """

    def test_index_page_status(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ChoicePageTestCase(TestCase):
    """
    This class tests the choice page view
    """
    # def test_choice_page(self):
    #     query = 'nutella'
    #     response = self.client.get(reverse('search:choice')))
    #     self.assertEqual(response.status_code, 200)
    pass

class ProductPageTestCase(TestCase):
    """
    This class tests the product page view
    """
    @classmethod
    def setUpTestData(cls):

        # We add two products
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
        ]
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

        # We add a user who registered the "Le jus de raisin 100% jus de fruits" product
        username = 'test-ref'
        mail = 'test-ref@register.com'
        password = 'ref-test-view'
        password_check = 'ref-test-view'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="123456789")
        user_profile.products.add(product.id)

    def test_product_page_get(self):
        code = Product.objects.get(ref="123456789").ref
        response = self.client.get(reverse('search:product', args=(code,)))
        self.assertEqual(response.status_code, 200)

    def test_product_page_user_product_registered(self):
        user = self.client.login(username='test-ref', password='ref-test-view')
        
        user = User.objects.get(username='test-ref')
        product_ref = [product.ref for product in user.profile.products.all()]
        print(product_ref)
        code = Product.objects.get(ref="123456789").ref
        response = self.client.get(reverse('search:product', args=(code,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product_registered'], True)

        

class RegisterPageTestCase(TestCase):
    """
    This class tests the register page view
    """
    
    @classmethod
    def setUpTestData(cls):
        username = 'test-ref'
        mail = 'test-ref@register.com'
        password = 'ref-test-view'
        password_check = 'ref-test-view'
        User.objects.create_user(username, mail, password)

    def test_register_page_get(self):
        response = self.client.get(reverse('search:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_success_registration(self):

        data = {
            'username' : 'test-page',
            'mail' : 'test-unitaire@register.com',
            'password' : 'test-unitaire-view',
            'password_check' : 'test-unitaire-view',
        }

        response = self.client.post(reverse('search:register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:log_in'))

    def test_register_page_fail_registration(self):
        data = {
            'username' : 'test-ref',
            'mail' : 'test-unitaire@register.com',
            'password' : 'test-unitaire-view',
            'password_check' : 'test-unitaire-view',
        }

        response = self.client.post(reverse('search:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], True)

class LoginPageTestCase(TestCase):
    """
    This class tests the log-in page view
    """

    @classmethod
    def setUpTestData(cls):
        username = 'username-existing'
        mail = 'test-ref@register.com'
        password = 'existing-ref'
        password_check = 'existing-ref'
        User.objects.create_user(username, mail, password)

    def test_login_page_get(self):
        response = self.client.get(reverse('search:log_in'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_success_connexion(self):

        data = {
            'username' : 'username-existing',
            'password' : 'existing-ref',
        }

        response = self.client.post(reverse('search:log_in'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:personal'))
    
    def test_login_page_fail_connexion_username(self):
        data = {
            'username' : 'unknown',
            'password' : 'existing-ref',
        }

        response = self.client.post(reverse('search:log_in'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], True)

    def test_login_page_fail_connexion_password(self):
        data = {
            'username' : 'username-existing',
            'password' : 'unknown-ref',
        }

        response = self.client.post(reverse('search:log_in'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], True)

class LogoutPageTestCase(TestCase):
    """
    This class tests the log-out page view
    """

    def test_logout_page(self):
        response = self.client.get(reverse('search:log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:log_in'))

class PersonalPageTestCase(TestCase):
    """
    This class tests the personal account page view
    """

    @classmethod
    def setUpTestData(cls):
        username = 'username-existing'
        mail = 'test-ref@register.com'
        password = 'existing-ref'
        password_check = 'existing-ref'
        User.objects.create_user(username, mail, password)

    def test_personal_page_connected(self):
        user = self.client.login(username='username-existing', password='existing-ref')
        response = self.client.get(reverse('search:personal'))
        self.assertEqual(response.status_code, 200)

    def test_personal_page_non_connected(self):
        response = self.client.get(reverse('search:personal'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/search/login?next=/search/personal-account')

class ProductRegisteredPageTestCase(TestCase):
    """
    This class tests the product-registered page view
    """
    
    @classmethod
    def setUpTestData(cls):
        username = 'username-existing'
        mail = 'test-ref@register.com'
        password = 'existing-ref'
        password_check = 'existing-ref'
        User.objects.create_user(username, mail, password)

    def test_product_registered_page_connected(self):
        user = self.client.login(username='username-existing', password='existing-ref')
        response = self.client.get(reverse('search:product_registered'))
        self.assertEqual(response.status_code, 200)

    def test_product_registered_page_non_connected(self):
        response = self.client.get(reverse('search:product_registered'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/search/login?next=/search/product-registered')