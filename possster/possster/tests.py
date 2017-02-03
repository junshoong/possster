from django.test import TestCase
from django.contrib.auth.models import User
from possster.forms import CustomUserCreationForm


class SetupClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="tester",
            password="qq12341234",
            email="tester@example.com",
        )


class CustomUserCreationFormTest(TestCase):
    def test_form_valid(self):
        form = CustomUserCreationForm(data={
            'username': 'tester',
            'email': 'tester@example.com',
            'password1': 'qq12341234',
            'password2': 'qq12341234',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CustomUserCreationForm(data={
            'username': 'tester',
            'email': '',
            'password1': 'qq',
            'password2': 'qq',
        })
        self.assertFalse(form.is_valid())


class UserCreationViewTest(SetupClass):
    def test_uses_register_template(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_add_user_invalid_form_view(self):
        response = self.client.post('/register/', {
            'username': 'tester',
            'email': 'tester@example.com',
            'password': 'qq12341234',
        })
        self.assertTrue("이미 존재", response.content.decode('utf-8'))

    def test_add_user_valid_form_view(self):
        user_count = User.objects.count()
        response = self.client.post('/register/', {
            'username': 'tester2',
            'email': 'tester2@example.com',
            'password1': 'qq12341234',
            'password2': 'qq12341234',
        }, follow=True)
        self.assertRedirects(response, '/register/done')
        self.assertEqual(User.objects.count(), user_count+1)


class UserDeleteViewTest(SetupClass):
    def test_user_delete_view(self):
        user_count = User.objects.count()
        user = User.objects.get(username='tester')
        response = self.client.post('/register/remove/'+str(user.pk)+'/', follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), user_count-1)
