from django.test import TestCase
from django.test import override_settings
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from poster.models import Poster
from possster.settings import BASE_DIR
from datetime import datetime
from datetime import timedelta
import os


@override_settings(MEDIA_ROOT='/tmp/django_test/')
class PosterModelTest(TestCase):

    _image = SimpleUploadedFile(name='test_image.jpg', content=None, content_type='image/jpeg')

    @staticmethod
    def _create_user():
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        return user

    def test_saving_and_retrieving_poster(self):
        user = self._create_user()
        first_poster = Poster()
        first_poster.title = 'first'
        first_poster.image = self._image
        first_poster.writer = user
        first_poster.save()

        second_poster = Poster()
        second_poster.title = 'second'
        second_poster.image = self._image
        second_poster.writer = user
        second_poster.save()

        saved_poster = Poster.objects.all()
        self.assertEqual(saved_poster.count(), 2)
        self.assertEqual(saved_poster[0].title, 'first')
        self.assertEqual(saved_poster[1].title, 'second')
        self.assertEqual(saved_poster[0].writer, user)

    def test_expired_poster(self):
        user = self._create_user()
        dt = timedelta(days=1)
        yesterday = datetime.now() - dt
        tomorrow = datetime.now() + dt

        expired_poster = Poster.objects.create(title='test_poster', image=self._image, writer=user, end=yesterday)
        self.assertTrue(expired_poster.is_over)

        not_expired_poster = Poster.objects.create(title='test_poster2', image=self._image, writer=user, end=tomorrow)
        self.assertFalse(not_expired_poster.is_over)

        no_end_poster = Poster.objects.create(title='test_poster2', image=self._image, writer=user)
        self.assertFalse(no_end_poster.is_over)

    def tearDown(self):
        import glob
        import os
        for f in glob.glob('/tmp/django_test/poster/*'):
            os.remove(f)


class PosterLVTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_uses_poster_list_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poster/poster_list.html')


@override_settings(MEDIA_ROOT='/tmp/django_test/')
class PosterEditTest(TestCase):

    _image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open(BASE_DIR+'/../testfile/test_image.jpg', 'rb').read(),
        content_type='image/jpeg'
    )

    @staticmethod
    def _create_user():
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        return user

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        import glob
        for f in glob.glob('/tmp/django_test/poster/*'):
            os.remove(f)

    def test_uses_poster_form_template(self):
        # 로그인 전
        response = self.client.get('/add/', follow=True)
        self.assertRedirects(response, '/login/?next=/add/')
        self.assertTemplateUsed(response, 'registration/login.html')

        # 로그인 후
        self._create_user()
        self.client.login(username='test', password='test')
        response = self.client.get('/add/')
        self.assertTemplateUsed(response, 'poster/poster_form.html')

    def test_can_save_a_POST_request(self):
        user = self._create_user()
        self.client.login(username='test', password='test')
        response = self.client.post(reverse_lazy('add'), {
            'title': "Test Poster 1",
            'image': self._image,
        })
        new_poster = Poster.objects.first()
        self.assertEqual(Poster.objects.count(), 1)
        self.assertEqual(new_poster.title, 'Test Poster 1')
        self.assertEqual(new_poster.writer, user)
        self.assertEqual(302, response.status_code)
