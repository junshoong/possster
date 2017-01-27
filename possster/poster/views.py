from django.views.generic import ListView
from poster.models import Poster


class PosterLV(ListView):
    model = Poster
    template_name = 'poster/poster_list.html'

