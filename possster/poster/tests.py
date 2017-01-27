from django.test import TestCase
from django.test import override_settings
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from poster.models import Poster
from datetime import datetime
from datetime import timedelta


@override_settings(MEDIA_ROOT='/tmp/django_test/')
class PosterModelTest(TestCase):

    _image = SimpleUploadedFile(name='test_image.jpg', content=None, content_type='image/jpeg')

    @staticmethod
    def _create_user():
        user = User.objects.create(username='test')
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
