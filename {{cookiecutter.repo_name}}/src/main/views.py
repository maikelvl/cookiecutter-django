from django.views.generic.base import TemplateView


class OpenSearchXMLView(TemplateView):
    template_name = 'search/opensearch.xml'
    content_type = 'application/opensearchdescription+xml'


class ErrorView(TemplateView):
    status_code = None

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        if self.status_code:
            response.status_code = self.status_code
        return response

    @classmethod
    def rendered_view(cls, **kwargs):
        v = cls.as_view(**kwargs)

        def view(request):
            response = v(request)
            response.render()
            return response
        return view
