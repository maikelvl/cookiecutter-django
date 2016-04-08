from django.db.models.fields import URLField

from main.widgets import CleanAdminURLFieldWidget


class AdminURLMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, URLField):
            kwargs = kwargs or {}
            kwargs['widget'] = CleanAdminURLFieldWidget
        return super(AdminURLMixin, self).formfield_for_dbfield(
            db_field, **kwargs)
