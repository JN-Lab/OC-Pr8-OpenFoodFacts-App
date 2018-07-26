from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User
from ..models import Product, Category, Profile

class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # We create a first user which registered one product
        username = 'test-functional'
        mail = 'test-functional@register.com'
        password = 'test-login-selenium'
        password_check = 'test-login-selenium'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test-functional')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test-login-selenium')
        self.selenium.find_element_by_css_selector(".btn-submit-user").click()