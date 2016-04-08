from decimal import Decimal

from django import forms
from django.http.request import QueryDict
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from main.templatetags import generic, mathtags
from main.templatetags.active import active, active_compare, active_reverse
from main.templatetags.svg import SvgNode


class GenericTagsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_filter_build_params(self):
        context = {'request': self.factory.get('/')}
        result = generic.filter_build_params(context, 'q', 'john')

        assert result == u'?q=john'

        context = {'request': self.factory.get('/?ot=asc&o=titel&test=a')}
        result = QueryDict(
            generic.filter_build_params(context, 'q', 'john')[1:])

        assert result['ot'] == 'asc'
        assert result['o'] == 'titel'
        assert result['q'] == 'john'

        context = {'request': self.factory.get('/')}
        QueryDict(generic.filter_build_params(context)[1:])

    def test_filter_active(self):
        context = {'request': self.factory.get('/?filter=B')}
        result = generic.filter_active(context, 'filter', 'A')
        assert result == ''

        context = {'request': self.factory.get('/?filter=A')}
        result = generic.filter_active(context, 'filter', 'A')
        assert result == 'active'

    def test_paginator_params(self):
        request = self.factory.get('/')

        context = {'request': request}
        result = generic.paginator_get_params(context, 1)

        assert result == u'?pagina=1'

        context['request'] = self.factory.get('/?pagina=5')
        assert QueryDict(generic.paginator_get_params(
            context, 2)) == QueryDict(u'?pagina=2')

        # TODO fix assert, random fail key order
        # context['request'] = self.factory.get('/?pagina=3&lorem=ipsum')
        # assert QueryDict(generic.paginator_get_params(
        #     context, 3)) == QueryDict(u'?pagina=3&lorem=ipsum')

        context['request'] = self.factory.get('/?pagina=50&_pjax=1')
        assert QueryDict(generic.paginator_get_params(
            context, 10)) == QueryDict(u'?pagina=10')

    def test_form_action_params(self):

        class DummyForm(forms.Form):
            chars = forms.CharField()
            email = forms.EmailField()
        form = DummyForm()

        request = self.factory.get('/')

        context = {'request': request}
        result = generic.form_action_params(context, form)

        assert result == u'?'

        context['request'] = self.factory.get('/?chars=abc')
        assert generic.form_action_params(context, form) == u'?'

        context['request'] = self.factory.get('/?chars=abc&lorem=ipsum&foo=1')
        assert generic.form_action_params(
            context, form, 'foo') == u'?lorem=ipsum'

        context['request'] = self.factory.get('/?email=qwerty&_pjax=1&chars=a')
        assert generic.form_action_params(context, form) == u'?'

    def test_replace(self):
        assert generic.replace('', None) == ''
        assert generic.replace('', '') == ''
        assert generic.replace('', 'a') == ''
        assert generic.replace('', 'a,') == ''
        assert generic.replace(None, 'b') == ''
        assert generic.replace('abcdef', 'bcd,') == 'aef'
        assert generic.replace('abcdef', 'bcd,xyz') == 'axyzef'

    def test_clean_url(self):
        c = generic.clean_url

        assert c('') == ''
        assert c(None) == ''
        assert c('None') == ''
        assert c('abcdef') == 'abcdef'
        assert c('localhost.nl') == 'localhost.nl'
        assert c('localhost.nl/') == 'localhost.nl'
        assert c('localhost.nl/?test') == 'localhost.nl'
        assert c('www.localhost.nl') == 'www.localhost.nl'
        assert c('www.localhost.nl/') == 'www.localhost.nl'
        assert c('www.localhost.nl/?test=a') == 'www.localhost.nl'
        assert c('www.localhost.nl/abc/def/') == 'www.localhost.nl'
        assert c('www.localhost.nl/abc/') == 'www.localhost.nl'
        assert c('www.localhost.nl/abc/?lorem=1') == 'www.localhost.nl'
        assert c('http://localhost.nl/abc/') == 'localhost.nl'
        assert c('http://localhost.nl/abc/?a=/') == 'localhost.nl'
        assert c('http://sub.localhost.nl/abc/') == 'sub.localhost.nl'
        assert c('https://sub.localhost.nl/abc/') == 'sub.localhost.nl'

    def test_bleach(self):
        assert generic.bleach_tags('') == ''
        assert generic.bleach_tags('<p>hoi</p>') == 'hoi'

        assert generic.bleach_tags(
            '<strong><!-- lorem -->dolor</strong>') == 'dolor'

        assert generic.bleach_tags(
            '<p style="border: 2px solid black;">hoi</p>') == 'hoi'

        assert generic.bleach_tags('< foo') == '&lt; foo'

    def test_trunc_number_with_dot(self):
        assert generic.trunc_number_with_dot(None) == ''
        assert generic.trunc_number_with_dot('') == ''
        assert generic.trunc_number_with_dot(' ') == ''
        assert generic.trunc_number_with_dot([]) == '[]'

        assert generic.trunc_number_with_dot(0) == '0.00'
        assert generic.trunc_number_with_dot(1) == '1.00'
        assert generic.trunc_number_with_dot(1, 2) == '1.00'
        assert generic.trunc_number_with_dot(1, 3) == '1.000'
        assert generic.trunc_number_with_dot(1, decimals=2) == '1.00'

        assert generic.trunc_number_with_dot(12, decimals=2) == '12.00'
        assert generic.trunc_number_with_dot(12, decimals=3) == '12.000'
        assert generic.trunc_number_with_dot(-12, decimals=3) == '-12.000'

        assert generic.trunc_number_with_dot(float(1)) == '1.00'
        assert generic.trunc_number_with_dot(float(5.03)) == '5.03'
        assert generic.trunc_number_with_dot(float(1243.9823)) == '1243.98'
        assert generic.trunc_number_with_dot(float(1243.9823), 1) == '1243.9'
        assert generic.trunc_number_with_dot(
            float(1243.9823), 3) == '1243.982'
        assert generic.trunc_number_with_dot(
            float(1243.9823), 8) == '1243.98230000'
        assert generic.trunc_number_with_dot(
            float(-1243.9823), 3) == '-1243.982'

        assert generic.trunc_number_with_dot(64.999) == '64.99'
        assert generic.trunc_number_with_dot(64.999, 3) == '64.999'
        assert generic.trunc_number_with_dot(64.95) == '64.95'
        assert generic.trunc_number_with_dot(-64.95) == '-64.95'

        assert generic.trunc_number_with_dot(Decimal(0)) == '0.00'
        assert generic.trunc_number_with_dot(Decimal(1)) == '1.00'
        assert generic.trunc_number_with_dot(Decimal('64.999')) == '64.99'
        assert generic.trunc_number_with_dot(Decimal('64.999'), 1) == '64.9'
        assert generic.trunc_number_with_dot(Decimal('64.999'), 2) == '64.99'
        assert generic.trunc_number_with_dot(Decimal('64.999'), 3) == '64.999'
        assert generic.trunc_number_with_dot(Decimal('64.999'), 4) == '64.9990'
        assert generic.trunc_number_with_dot(Decimal('64.95')) == '64.95'
        assert generic.trunc_number_with_dot(Decimal('-64.95')) == '-64.95'

        assert generic.trunc_number_with_dot('0') == '0.00'
        assert generic.trunc_number_with_dot('0.00') == '0.00'
        assert generic.trunc_number_with_dot('0,00') == '0.00'
        assert generic.trunc_number_with_dot('10') == '10.00'
        assert generic.trunc_number_with_dot('10', 3) == '10.000'
        assert generic.trunc_number_with_dot('10.01', 1) == '10.0'
        assert generic.trunc_number_with_dot('10.01', 2) == '10.01'
        assert generic.trunc_number_with_dot('10.01', 3) == '10.010'
        assert generic.trunc_number_with_dot('10.01', 4) == '10.0100'
        assert generic.trunc_number_with_dot('10.01', 5) == '10.01000'


class ActiveTagsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_active(self):
        assert active({'request': self.factory.get('/')}, '') == 'active'

        assert active({
            'request': self.factory.get('/')}, 'lorem') == ''
        assert active({
            'request': self.factory.get('configuratie')}, 'configuratie') == ''

        assert active({
            'request': self.factory.get('/configuratie/')
        }, '/configuratie') == 'active'

        assert active({
            'request': self.factory.get('/configuratie/')
        }, '/configuratie/') == 'active'

        assert active({
            'request': self.factory.get('/configuratie/')
        }, '/configuratie/', 'huidig') == 'huidig'

    def test_active_reverse(self):
        assert active_reverse({
            'request': self.factory.get('/')
        }, 'home') == 'active'

        assert active_reverse({
            'request': self.factory.get('/')
        }, 'home', 'actief') == 'actief'

        assert active_reverse({
            'request': self.factory.get('/loremdolor/')
        }, 'search') == ''

    def test_active_compare(self):
        assert active_compare("auto", "auto") == 'active'
        assert active_compare("auto", "auto", "camper") == 'active'

        assert active_compare("aut", "auto") == ''
        assert active_compare("aut", "auto", "camper") == ''

        assert active_compare("auto", "auto", class_name='huidig') == 'huidig'
        assert active_compare("auto", "auto", "active",
                              class_name='huidig') == 'huidig'


class MathTagsTestCase(TestCase):

    def test_multiply(self):
        assert mathtags.mult(4, "2") == 8.0
        assert mathtags.mult(4, 2) == 8.0
        assert mathtags.mult(5.5, 2) == 11.0
        assert mathtags.mult(10, 2.5) == 20  # argument is cast to int

        with self.assertRaises(ValueError):
            mathtags.mult("", 1)

        with self.assertRaises(ValueError):
            mathtags.mult("abc", 2)

        with self.assertRaises(TypeError):
            mathtags.mult(None, 5)

        with self.assertRaises(ValueError):
            mathtags.mult(10, "abc")

        with self.assertRaises(ValueError):
            mathtags.mult(10, "")

        with self.assertRaises(TypeError):
            mathtags.mult(10, None)

    def test_subtract(self):
        assert mathtags.sub(4, "2") == 2.0
        assert mathtags.sub(4, 2) == 2.0
        assert mathtags.sub(5.5, 2) == 3.5
        assert mathtags.sub(10, 2.5) == 8  # argument is cast to int

        with self.assertRaises(ValueError):
            mathtags.sub("", 1)

        with self.assertRaises(ValueError):
            mathtags.sub("abc", 2)

        with self.assertRaises(TypeError):
            mathtags.sub(None, 5)

        with self.assertRaises(ValueError):
            mathtags.sub(10, "abc")

        with self.assertRaises(ValueError):
            mathtags.sub(10, "")

        with self.assertRaises(TypeError):
            mathtags.sub(10, None)

    def test_divide(self):
        assert mathtags.div(7, "2") == 3.5
        assert mathtags.div(4, 2) == 2.0
        assert mathtags.div(5.5, 2) == 2.75
        assert mathtags.div(10, 2.5) == 5  # argument is cast to int

        with self.assertRaises(ValueError):
            mathtags.div("", 1)

        with self.assertRaises(ValueError):
            mathtags.div("abc", 2)

        with self.assertRaises(TypeError):
            mathtags.div(None, 5)

        with self.assertRaises(ValueError):
            mathtags.div(10, "abc")

        with self.assertRaises(ValueError):
            mathtags.div(10, "")

        with self.assertRaises(TypeError):
            mathtags.div(10, None)

    def test_ceil(self):
        assert mathtags.ceil(7) == 7.0
        assert mathtags.ceil(4) == 4
        assert mathtags.ceil(5.5) == 6
        assert mathtags.ceil(5.4) == 6
        assert mathtags.ceil(10.01) == 11
        assert mathtags.ceil(10) == 10

        with self.assertRaises(ValueError):
            mathtags.ceil("")

        with self.assertRaises(ValueError):
            mathtags.ceil("abc")

        with self.assertRaises(TypeError):
            mathtags.ceil(None)

    def test_add_float(self):
        assert mathtags.addf(7, "2") == 9.0
        assert mathtags.addf(4, 2) == 6.0
        assert mathtags.addf(5.5, 2) == 7.5
        assert mathtags.addf(10, 2.5) == 12.5
        assert mathtags.addf(10.5, 2.5) == 13

        with self.assertRaises(ValueError):
            mathtags.addf("", 1)

        with self.assertRaises(ValueError):
            mathtags.addf("abc", 2)

        with self.assertRaises(TypeError):
            mathtags.addf(None, 5)

        with self.assertRaises(ValueError):
            mathtags.addf(10, "abc")

        with self.assertRaises(ValueError):
            mathtags.addf(10, "")

        with self.assertRaises(TypeError):
            mathtags.addf(10, None)
