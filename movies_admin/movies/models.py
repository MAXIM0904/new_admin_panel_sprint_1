import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeCreatedMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date of creation'))

    class Meta:
        abstract = True


class TimeModifiedMixin(TimeCreatedMixin):
    modified = models.DateTimeField(
        auto_now=True, verbose_name=_('Date of change'))

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name=_('record ID'))

    class Meta:
        abstract = True


class FilmWork(UUIDMixin, TimeModifiedMixin):
    title = models.CharField(_('Title film'), max_length=255)
    description = models.TextField(
        _('Description film'), blank=True, null=True)
    creation_date = models.DateTimeField(
        _('Creation date film'), auto_now_add=True)
    rating = models.FloatField(_('Rating'))
    type = models.TextField(_('Type'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title


class FilmWorkMixin(models.Model):
    film_work = models.ForeignKey(
        FilmWork, on_delete=models.CASCADE, verbose_name=_('Film work'))

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeModifiedMixin):
    name = models.CharField(_('Name genre'), max_length=255)
    description = models.TextField(_('Description genre'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeModifiedMixin):
    full_name = models.CharField(_('Full name person'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class GenreFilmWork(UUIDMixin, TimeCreatedMixin, FilmWorkMixin):
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name=_('Title'))

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('title')
        verbose_name_plural = _('title')

    def __str__(self):
        return str(self.genre)


class PersonFilmWork(UUIDMixin, TimeCreatedMixin, FilmWorkMixin):
    role = models.TextField(_('Role'), blank=True, null=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name=_('Person'))

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _("The actor's connection to the film")
        verbose_name_plural = _("The actor's connection with films")

    def __str__(self):
        return self.role
