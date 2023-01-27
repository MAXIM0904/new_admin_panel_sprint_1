from django.contrib import admin
from .models import Genre, PersonFilmWork, Person, FilmWork, GenreFilmWork
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [
        PersonFilmWorkInline,
    ]
    list_display = ('full_name', 'created', 'modified')
    list_display_links = ('full_name', )
    search_fields = ('full_name', 'created', 'modified')


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = [
        GenreFilmWorkInline,
    ]
    list_display = ('name', 'description', 'created', 'modified')


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = [
        PersonFilmWorkInline,
        GenreFilmWorkInline,
    ]
    list_display = ('title', 'description', 'creation_date',
                    'rating', 'type', 'created', 'modified')
    list_display_links = ('title', 'description', 'rating', 'type')
    search_fields = ('description', 'rating', 'type')
    list_filter = ('type',)


admin.site.site_title = _('Online cinema Admin Panel')
admin.site.site_header = _('Online cinema Admin Panel')
admin.site.unregister(Group)
admin.site.unregister(User)
