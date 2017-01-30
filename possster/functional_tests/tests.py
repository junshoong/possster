from django.test import LiveServerTestCase
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from possster.settings import BASE_DIR
from django.contrib.auth.models import User
import time

TEST_ID = 'tester'
TEST_PW = 'qq12341234'
TEST_EMAIL = 'tester@example.com'


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


@override_settings(MEDIA_ROOT='/tmp/django_test/')
class NewVisitorTest(LiveServerTestCase):

    @staticmethod
    def _create_user():
        user = User.objects.create(username=TEST_ID)
        user.set_password(TEST_PW)
        user.save()
        return user

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        import glob
        import os
        for f in glob.glob('/tmp/django_test/poster/*'):
            os.remove(f)

    def test_open_browser(self):
        # self._create_user()
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더를 확인합니다.
        self.assertIn('Possster', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Possster', header.text)

        # 회원가입 링크로 이동합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('회원가입').click()
        self.assertIn('회원가입', self.browser.title)

        # 주어진 필드에 값을 입력합니다.
        username = self.browser.find_element_by_id('id_username')
        username.send_keys(TEST_ID)

        email = self.browser.find_element_by_id('id_email')
        email.send_keys(TEST_EMAIL)

        password1 = self.browser.find_element_by_id('id_password1')
        password1.send_keys(TEST_PW)

        password2 = self.browser.find_element_by_id('id_password2')
        password2.send_keys(TEST_PW)

        # 회원가입을 누르면 계정이 등록되고 등록완료 화면으로 이동됩니다.
        with wait_for_page_load(self.browser):
            password2.send_keys(Keys.ENTER)
        self.assertIn('회원가입완료', self.browser.title)

        # 홈 화면으로 이동합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('홈 화면').click()
        self.assertIn('Possster', self.browser.title)

        # 로그인 버튼을 눌러 로그인 화면으로 이동합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('로그인').click()
        self.assertIn('로그인', self.browser.title)

        # ID와 PW를 입력하고 로그인합니다.
        login_id = self.browser.find_element_by_id('id_username')
        login_id.send_keys(TEST_ID)

        login_pw = self.browser.find_element_by_id('id_password')
        login_pw.send_keys(TEST_PW)
        login_pw.send_keys(Keys.ENTER)

        # 메인화면으로 돌아와서 로그인이 되었는지 확인합니다.
        account_link = self.browser.find_element_by_link_text(TEST_ID)
        self.assertEqual(account_link.text, TEST_ID)

        # upload 버튼을 눌러 포스터를 새로 등록하는 화면으로 이동합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('업로드').click()
        self.assertIn('업로드', self.browser.title)

        # 내용을 채우고 등록버튼을 눌러 포스터를 등록합니다.
        input_title = self.browser.find_element_by_id('id_title')
        input_title.send_keys('Test Poster')

        input_image = self.browser.find_element_by_id('id_image')
        input_image.send_keys(BASE_DIR+'/../testfile/test_image.jpg')

        self.browser.find_element_by_xpath(
            "//input[@type='submit' and @value='저장']"
        ).click()

        # 메인화면으로 돌아가 등록된 포스터를 확인합니다.
        first_image = self.browser.find_elements_by_tag_name('img')[0]
        self.assertIn('test_image', first_image.get_attribute('src'))

        # 로그아웃을 합니다.
        with wait_for_page_load(self.browser):
            self.browser.find_element_by_link_text('로그아웃').click()
        self.assertIn('로그아웃', self.browser.title)
