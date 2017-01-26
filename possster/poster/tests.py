from django.test import TestCase
from possster.settings import MEDIA_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from poster.models import Poster
from datetime import datetime
from datetime import timedelta
import glob
import os


class PosterTest(TestCase):

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

        expired_poster = Poster.objects.create(title='test_poster2', image=self._image, writer=user, end=tomorrow)
        self.assertFalse(expired_poster.is_over)

    def tearDown(self):
        for f in glob.glob(MEDIA_ROOT+'/poster/test_image*.jpg'):
            os.remove(f)

