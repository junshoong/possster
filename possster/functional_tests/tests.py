from django.test import LiveServerTestCase
from selenium import webdriver
from possster.settings import BASE_DIR
from django.contrib.auth.models import User
import time


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class wait_for_page_load(object):
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)


class NewVisitorTest(LiveServerTestCase):

    @staticmethod
    def _create_user():
        user = User.objects.create(username='test')
        return user

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_open_browser(self):
        user = self._create_user()
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더를 확인합니다.
        self.assertIn('Possster', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Possster', header.text)

        # upload 버튼을 눌러 포스터를 새로 등록하는 화면으로 이동합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('업로드').click()
        self.assertIn('업로드', self.browser.title)

        # 내용을 채우고 등록버튼을 눌러 포스터를 등록합니다.
        input_title = self.browser.find_element_by_id('id_title')
        input_title.send_keys('Test Poster')

        input_image = self.browser.find_element_by_id('id_image')
        input_image.send_keys(BASE_DIR+'/media/testfile/test_image.jpg')

        input_writer = self.browser.find_element_by_id('id_writer')
        input_writer.send_keys('test')

        self.browser.find_element_by_xpath(
            "//input[@type='submit' and @value='저장']"
        ).click()

        # 메인화면으로 돌아가 등록된 포스터를 확인합니다.
        first_image = self.browser.find_elements_by_tag_name('img')[0]
        self.assertIn('test_image', first_image.get_attribute('src'))
