from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from possster.forms import CustomUserCreationForm
from django.contrib.auth.models import User


class UserCV(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


class UserTV(TemplateView):
    model = User
    template_name = 'registration/mypage.html'


class UserDV(DeleteView):
    model = User
    success_url = reverse_lazy('index')
    template_name = 'registration/user_confirm_delete.html'
