from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from poster.models import Poster


class PosterLV(ListView):
    model = Poster
    template_name = 'poster/poster_list.html'
    context_object_name = 'poster'


class PosterCV(CreateView):
    model = Poster
    fields = ('title', 'image', 'end', 'writer')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.writer = self.request.user
        return super(PosterCV, self).form_valid(form)
