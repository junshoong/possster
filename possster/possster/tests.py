from django.test import TestCase
from selenium import webdriver


class HomeViewTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_open_browser(self):
        self.browser.get('http://localhost:8000')
        self.assertIn("Possster", self.browser.title)
