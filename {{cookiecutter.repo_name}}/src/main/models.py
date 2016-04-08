from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.urlresolvers import NoReverseMatch
from django.db import models
from django.template.defaultfilters import slugify
from django.test.client import Client
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField
from sorl.thumbnail.fields import ImageField

from main.utils import generate_filename

from .utils import now_no_micro


class SlugModel(models.Model):

    slug = models.SlugField(_('slug'), max_length=150, unique=True)

    class Meta:
        abstract = True

    def clean(self):
        self.slug = self.slug.lower()

        # Check if slug doesnt create an already in use url
        if not self.pk or \
                self.slug != self._default_manager.get(pk=self.pk).slug:

            client = Client()
            try:
                response = client.get(self.get_absolute_url(), follow=True)

                if response.status_code != 404:
                    raise ValidationError({
                        'slug': _('Er is al een pagina bekend in het systeem '
                                  'met de naam "{}".'
                                  .format(self.get_absolute_url()))
                    })
            except (NoReverseMatch, AttributeError):
                pass


class AutoSlugModel(models.Model):
    slug = models.SlugField(
        _('slug'), max_length=255, unique=True, editable=False)

    _slugified_value = ('title',)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):

        if hasattr(self, 'slug_list'):
            slug_list = self.slug_list
        else:
            slug_list = (getattr(self, atr) for atr in self._slugified_value)

        self.slug = slugify(' '.join(filter(None, slug_list)))

        slug_base = '{}-{}'.format(self.slug, '{}').format

        def get_qs():
            qs = self.__class__.objects.filter(slug__iexact=self.slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            return qs

        i = 0
        while get_qs().exists():
            i += 1
            self.slug = slug_base(i)


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return force_text(self._meta.verbose_name)

    @classmethod
    def singleton(cls):
        return cls.objects.first() or cls.objects.create()


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """
    def pre_save(self, model_instance, add):
        value = now_no_micro()
        setattr(model_instance, self.attname, value)
        return value


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(
        _('aanmaakdatum'), editable=True, default=now_no_micro)
    modified = AutoLastModifiedField(
        _('aanpasdatum'), editable=True, default=now_no_micro)

    class Meta:
        abstract = True


class AddressModel(models.Model):

    street = models.CharField(_('straat'), max_length=150, null=True,
                              blank=True)
    house_number = models.CharField(_('huisnummer'), max_length=30, null=True,
                                    blank=True)
    postal_code = models.CharField(_('postcode'), max_length=6, null=True,
                                   blank=True)
    city = models.CharField(_('plaats'), max_length=30, null=True, blank=True)

    class Meta:
        abstract = True


class MetaDescriptionModel(models.Model):

    meta_description = models.CharField(
        _('meta omschrijving'), max_length=150, blank=True)

    class Meta:
        abstract = True


class InlineImage(models.Model):
    image = ImageField(
        _('afbeelding'), upload_to=generate_filename,
        width_field='image_width', height_field='image_height')

    image_width = models.PositiveIntegerField(
        _('afbeelding breedte'), null=True, blank=True, editable=False)
    image_height = models.PositiveIntegerField(
        _('afbeelding hoogte'), null=True, blank=True, editable=False)

    alt_text = models.CharField(
        _('afbeelding omschrijving'), max_length=120,
        help_text=_('Omschrijf hier wat er te zien is op de afbeelding.'))

    caption = models.CharField(
        _('onderschrift'), max_length=2048, blank=True,
        help_text=_('Dit is een optionele tekst dat onder de afbeelding '
                    'getoond zal worden.'))

    url = models.URLField(_('URL'), max_length=2000, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('losse afbeelding')
        verbose_name_plural = _('losse afbeeldingen')

        ordering = ('pk',)

    def __str__(self):
        return self.alt_text

    @property
    def upload_to(self):
        return 'inline-images/%Y/%m/%d/'
