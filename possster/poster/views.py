from django.views.generic import ListView
from django.views.generic.edit import CreateView
from poster.models import Poster


class PosterLV(ListView):
    model = Poster
    template_name = 'poster/poster_list.html'


class PosterCV(CreateView):
    model = Poster
    fields = ('title', 'image', 'end')
