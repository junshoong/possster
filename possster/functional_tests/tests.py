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

        # 타이틀과 헤더를 확인합니다.
        self.assertIn('Possster', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Possster', header.text)

        # upload 버튼을 눌러 포스터를 새로 등록하는 화면으로 이동합니다.
        # 내용을 채우고 등록버튼을 눌러 포스터를 등록합니다.
        # 메인화면으로 돌아가 등록된 포스터를 확인합니다.
