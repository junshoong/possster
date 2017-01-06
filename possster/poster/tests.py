from django.test import TestCase
from poster.models import PosterCategory


class PosterCategoryTest(TestCase):

    def test_saving_and_retrieving_poster_category(self):
        first_category = PosterCategory()
        first_category.name = 'first'
        first_category.save()

        second = PosterCategory()
        second.name = 'second'
        second.save()

        saved_category = PosterCategory.objects.all()
        self.assertEqual(saved_category.count(), 2)

        self.assertEqual(saved_category[0].name, 'first')
        self.assertEqual(saved_category[1].name, 'second')
