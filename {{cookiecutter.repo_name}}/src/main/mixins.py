from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class SuccessMessageMixin(object):

    def get_success_message(self, cleaned_data):
        raise NotImplementedError

    def _add_success_message(self, cleaned_data):
        messages.success(self.request, self.get_success_message(cleaned_data))

    def form_valid(self, form):
        response = super().form_valid(form)
        self._add_success_message(form.cleaned_data)
        return response


class InvalidMessageMixin(object):

    def get_invalid_message(self, cleaned_data):
        return _('Niet alle verplichte velden zijn (correct) ingevuld.')

    def _add_invalid_message(self, cleaned_data):
        messages.error(self.request, self.get_invalid_message(cleaned_data))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        self._add_invalid_message(form.cleaned_data)
        return response
