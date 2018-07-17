#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..views import index, choice
from ..utils.treatment import Treatment

class IndexPageTestCase(TestCase):

    def test_index_page_status(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ChoicePageTestCase(TestCase):

    # def test_choice_page(self):
    #     query = 'nutella'
    #     response = self.client.get(reverse('search:choice')))
    #     self.assertEqual(response.status_code, 200)
    pass

class RegisterPageTestCase(TestCase):
    
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

    def test_logout_page(self):
        response = self.client.get(reverse('search:log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:log_in'))

class PersonalPageTestCase(TestCase):

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
        self.assertRedirects(response, '/search/login?next=/search/personal')