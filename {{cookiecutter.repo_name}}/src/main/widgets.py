from django.forms import TextInput

class CleanAdminURLFieldWidget(TextInput):
    def render(self, name, value, attrs=None):
        html = super(CleanAdminURLFieldWidget, self).render(name, value, attrs)
        return html
