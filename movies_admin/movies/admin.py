from django.contrib import admin
from .models import Genre, PersonFilmWork, Person, FilmWork, GenreFilmWork
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_display_links = ('full_name', )
    search_fields = ('full_name', 'created', 'modified')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name', ]


@admin.register(GenreFilmWork)
class GenreFilmWorkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre')
    autocomplete_fields = ['genre', 'film_work']


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'creation_date',
                    'rating', 'type', 'created', 'modified')
    list_display_links = ('title', 'description', 'rating', 'type')
    search_fields = ('description', 'rating', 'type')
    list_filter = ('type',)


@admin.register(PersonFilmWork)
class PersonFilmWorkInline(admin.ModelAdmin):
    list_display = ('person', 'role', 'created')
    autocomplete_fields = ['person', 'film_work']


admin.site.site_title = _('Online cinema Admin Panel')
admin.site.site_header = _('Online cinema Admin Panel')
admin.site.unregister(Group)
admin.site.unregister(User)
