from django.contrib import admin
from poster.models import Poster


class PosterAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'end')

admin.site.register(Poster, PosterAdmin)
