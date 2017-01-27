from django.test import LiveServerTestCase
from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_open_browser(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Possster", self.browser.title)
