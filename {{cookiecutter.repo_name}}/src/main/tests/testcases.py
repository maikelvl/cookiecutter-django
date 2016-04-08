from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.models.fields import AutoField
from django.utils import six
from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class LoginRequiredTestCaseMixin(object):
    url = None

    def setUp(self):
        super().setUp()

        User.objects.create_user(
            email='user@mediamoose.nl', password='test', first_name='Normal',
            last_name='User')
        self.client.login(username='user@mediamoose.nl', password='test')

    def _get_url(self):
        return self.url or super()._get_url()

    def test_login_required(self):
        url = self._get_url()

        resp = self.client.get(url)
        assert resp.status_code == 200

        self.client.logout()

        resp = self.client.get(url)
        assert resp.status_code == 302

        resp = self.client.get(url, follow=True)
        assert resp.status_code == 200
        assert resp.wsgi_request.GET.get('next') == url


class SuperuserRequiredTestCaseMixin(LoginRequiredTestCaseMixin):

    def setUp(self):
        super().setUp()

        User.objects.create_superuser(
            email='superuser@mediamoose.nl', password='test',
            first_name='Super', last_name='User')

        self.client.login(username='superuser@mediamoose.nl', password='test')

    def test_superuser_required(self):
        url = self._get_url()

        self.client.login(username='user@mediamoose.nl', password='test')

        resp = self.client.get(url)
        assert resp.status_code == 403


class TemplateViewTestCaseMixin(object):
    url = None
    url_name = i = None
    not_allowed_methods = ('post', 'put', 'patch', 'delete')

    def _get_url(self):
        return self.url

    def test_url_name(self):
        if self.url_name:
            assert reverse(self.url_name) == self._get_url()

    def test_template_view(self):
        url = self._get_url()
        resp = self.client.get(url)

        assert resp.status_code == 200

    def test_template_view_redirect(self):
        if not self._get_url()[-1:] == '/':
            return

        url = self._get_url().rstrip('/')
        if not url:
            return

        resp = self.client.get(url)
        assert resp.status_code == 301

        resp = self.client.get(url, follow=True)
        assert resp.status_code == 200

    def test_template_view_not_allowed(self):
        url = self._get_url()

        for method in self.not_allowed_methods:
            client_function = getattr(self.client, method)
            resp = client_function(url)
            assert resp.status_code == 405, \
                "Method '{}' should not be allowed.".format(method)


class DetailViewTestCaseMixin(object):
    detail_view_url = None
    test_get_absolute_url = True
    sitemap_url = None
    not_allowed_methods = ('post', 'put', 'patch', 'delete')

    def get_item(self):
        raise NotImplementedError

    def setUp(self):
        self.item = self.get_item()

    def _get_url(self):
        return self.detail_view_url or (
            self.item.get_absolute_url() if
            hasattr(self.item, 'get_absolute_url') else None)

    def test_object_url(self):
        if not self.test_get_absolute_url:
            return

        assert hasattr(self.item, 'get_absolute_url')

        url = self.item.get_absolute_url()

        assert isinstance(url, six.string_types)
        assert url == self._get_url()
        assert url.startswith('/')

    def test_detail_view(self):
        url = self._get_url()
        resp = self.client.get(url)

        assert resp.status_code == 200
        assert 'object' in resp.context
        assert resp.context['object'] == self.item

    def test_detail_view_redirect(self):
        url = self._get_url().rstrip('/')

        resp = self.client.get(url)
        assert resp.status_code == 301

        resp = self.client.get(url, follow=True)
        assert resp.status_code == 200

    def test_detail_view_not_allowed(self):
        url = self._get_url()

        for method in self.not_allowed_methods:
            client_function = getattr(self.client, method)
            resp = client_function(url)
            assert resp.status_code == 405

    def test_in_sitemap(self):
        if not self.sitemap_url:
            return

        resp = self.client.get(self.sitemap_url)
        assert resp.status_code == 200

        self.assertContains(resp, self.item.get_absolute_url())


class ListViewTestCaseMixin(object):
    list_view_url = None
    test_get_absolute_url = True
    not_allowed_methods = ('post', 'put', 'patch', 'delete')
    test_pagination = True

    def get_items(self):
        raise NotImplementedError

    def setUp(self):
        self.items = self.get_items()
        if self.test_pagination and len(self.items) < 2:
            self.fail("Cannot test pagination with less than two items.")

    def test_list_view(self):
        resp = self.client.get(self.list_view_url)

        assert resp.status_code == 200
        assert resp['Content-Type'] == 'text/html; charset=utf-8'
        assert 'object_list' in resp.context
        assert 'is_paginated' in resp.context

        if self.test_pagination:
            assert 'paginator' in resp.context
        else:
            assert all(item in resp.context['object_list']
                       for item in self.items)

        if resp.context['view'].paginate_by:
            assert isinstance(resp.context['view'].page_kwarg, Promise), \
                "Page kwarg of '{}' is not translated.".format(
                    resp.context['view'])

    def test_pages(self):
        if not self.test_pagination:
            return

        session = self.client.session
        session['paginate_by'] = 1
        session.save()

        resp = self.client.get(self.list_view_url)
        page_kwargs = resp.context['view'].page_kwarg
        paginator = resp.context['paginator']
        page_range = list(paginator.page_range)

        seen = set()
        for index, page_nr in enumerate(page_range, start=1):
            resp = self.client.get('{}?{}={}'.format(
                self.list_view_url, page_kwargs, page_nr))
            assert resp.status_code == 200
            assert resp['Content-Type'] == 'text/html; charset=utf-8'

            assert 'page_obj' in resp.context
            assert resp.context['page_obj'].number == index

            page_objects = resp.context['object_list']

            orphans = resp.context['view'].paginate_orphans
            if orphans:
                if page_nr == page_range[-1]:
                    assert 1 <= len(page_objects) <= 1 + orphans
                else:
                    assert len(page_objects) == 1
            else:
                assert len(page_objects) == 1
            seen.update(page_objects)

        assert len(seen) == len(self.items)

    def test_paginate_by(self):
        if not self.test_pagination:
            return

        session = self.client.session
        session['paginate_by'] = 1
        session.save()

        resp = self.client.get(self.list_view_url)
        paginator = resp.context['paginator']

        assert 1 <= paginator.num_pages <= len(self.items)

    def test_paginate_by_get_param(self):
        if not self.test_pagination:
            return

        resp = self.client.get('{}?{}=1'.format(
            self.list_view_url, _('aantal')))
        session = self.client.session

        assert resp.status_code == 200
        assert 'paginate_by' in session
        assert int(session['paginate_by']) == 1

    def test_invalid_paginate_by_in_session(self):
        if not self.test_pagination:
            return

        session = self.client.session
        session['paginate_by'] = 'test'
        session.save()

        resp = self.client.get(self.list_view_url)
        session = self.client.session

        assert resp.status_code == 200
        assert resp.context['page_obj'].number == 1
        assert session['paginate_by'] != 'test'

    def test_invalid_paginate_by_get_param(self):
        if not self.test_pagination:
            return

        resp = self.client.get('{}?{}=lorem'.format(
            self.list_view_url, _('aantal')))
        session = self.client.session

        assert resp.status_code == 200
        assert resp.context['page_obj'].number == 1
        assert session['paginate_by'] != 'lorem'

    def test_list_view_redirect(self):
        url = self.list_view_url.rstrip('/')

        resp = self.client.get(url)
        assert resp.status_code == 301

        resp = self.client.get(url, follow=True)
        assert resp.status_code == 200

    def test_list_view_not_allowed(self):
        for method in self.not_allowed_methods:
            client_function = getattr(self.client, method)
            resp = client_function(self.list_view_url)
            assert resp.status_code == 405

    def test_object_urls(self):
        if not self.test_get_absolute_url:
            return

        assert all(hasattr(item, 'get_absolute_url') for item in self.items)
        assert all(bool(item.get_absolute_url()) for item in self.items)

        resp = self.client.get(self.list_view_url)
        for item in self.items:
            url = item.get_absolute_url()
            self.assertContains(resp, url)


class ModelTestCaseMixin(object):
    test_get_absolute_url = True

    def get_item(self):
        raise NotImplementedError

    def setUp(self):
        item = self.get_item()
        self.item = item.__class__.objects.get(pk=item.pk)

    def test_unicode(self):
        try:
            str(self.item)
        except:
            self.fail()

    def test_translations(self):
        assert isinstance(self.item._meta.verbose_name, Promise), \
            "Verbose name not translated."
        assert isinstance(self.item._meta.verbose_name_plural, Promise), \
            "Verbose name plural not translated."

        for field in self.item._meta.get_fields():
            if isinstance(field, AutoField):
                continue
            try:
                field = field.field
            except AttributeError:
                pass
            assert isinstance(field.verbose_name, Promise), \
                "Field '{}' has no translated verbose name".format(field.name)

    def test_slug(self):
        if hasattr(self.item, 'slug'):
            assert isinstance(self.item.slug, six.string_types)

            if hasattr(self.item, 'create_slug'):
                self.slug = None
                self.item.create_slug()
                assert isinstance(self.item.slug, six.string_types)

            if hasattr(self.item, 'get_absolute_url'):
                assert self.item.slug in self.item.get_absolute_url()

    def test_url(self):
        if not self.test_get_absolute_url:
            return
        assert hasattr(self.item, 'get_absolute_url')
        assert isinstance(self.item.get_absolute_url(), six.string_types)


class CreateViewTestCaseMixin(object):
    create_view_url = None
    redirect_url = None
    not_allowed_methods = ('patch', 'delete')
    test_success_message = True
    form_data = None

    def get_form_data(self):
        return None

    def check_created_object(self):
        pass

    def test_create_view(self):
        url = self.create_view_url
        resp = self.client.get(url)

        assert resp.status_code == 200
        assert 'form' in resp.context

    def test_create_object(self):
        post_data = self.form_data
        if post_data is None:
            return

        url = self.create_view_url

        if self.redirect_url:
            resp = self.client.post(url, post_data, follow=True)
            self.assertRedirects(resp, self.redirect_url)
        else:
            resp = self.client.post(url, post_data, follow=True)
            assert resp.status_code == 200

        if self.test_success_message:
            assert 'messages' in resp.context
            assert len(resp.context['messages']) == 1
            assert any(message.level_tag == 'success' for message in
                       resp.context['messages'])

        self.check_created_object()

    def test_create_view_redirect(self):
        url = self.create_view_url.rstrip('/')

        resp = self.client.get(url)
        assert resp.status_code == 301

        resp = self.client.get(url, follow=True)
        assert resp.status_code == 200

    def test_create_view_not_allowed(self):
        url = self.create_view_url

        for method in self.not_allowed_methods:
            client_function = getattr(self.client, method)
            resp = client_function(url)
            assert resp.status_code == 405


class UpdateViewTestCaseMixin(DetailViewTestCaseMixin):
    not_allowed_methods = ('patch', 'delete')
    redirect_url = None
    test_success_message = True

    def test_update_view(self):
        url = self._get_url()
        resp = self.client.get(url)

        assert resp.status_code == 200
        assert 'form' in resp.context

    def get_form_data(self):
        return None

    def check_updated_object(self):
        pass

    def test_update_object(self):
        post_data = self.get_form_data()
        if post_data is None:
            return

        url = self._get_url()
        resp = self.client.post(url, post_data, follow=True)
        self.assertRedirects(resp, self.redirect_url or url)

        if self.test_success_message:
            assert 'messages' in resp.context
            assert len(resp.context['messages']) == 1
            assert any(message.level_tag == 'success' for message in
                       resp.context['messages'])

        self.check_updated_object()


class DeleteViewTestCaseMixin(DetailViewTestCaseMixin):
    not_allowed_methods = ('patch',)
    redirect_url = None
    test_success_message = True
    test_get_absolute_url = False

    def test_delete_view(self):
        url = self._get_url()
        resp = self.client.get(url)

        assert resp.status_code == 200
        assert 'can_delete' in resp.context

    def check_deleted_object(self):
        pass

    def test_delete_object(self):
        url = self._get_url()
        resp = self.client.delete(url, {}, follow=True)
        self.assertRedirects(resp, self.redirect_url)

        if self.test_success_message:
            assert 'messages' in resp.context
            assert len(resp.context['messages']) == 1
            assert any(message.level_tag == 'success' for message in
                       resp.context['messages'])

        self.check_deleted_object()

    def test_post_fallback(self):
        url = self._get_url()
        resp = self.client.post(url, {}, follow=True)
        self.assertRedirects(resp, self.redirect_url)

        self.check_deleted_object()
