import os
import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import shortstack.wsgi


class TestWSGI(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        self.test_project = os.path.join(module_path, 'testproject')

        self.app = shortstack.wsgi.Shortstack('shortstack', instance_path=self.test_project)
        self.client = Client(self.app, BaseResponse)

    def test_render_through_app(self):
        look_for = "This text only exists in the base template"
        response_implied_index = self.client.get('/')
        response_explicit_index = self.client.get('/index.html')

        self.assertIn(look_for, str(response_implied_index.data)) 
        self.assertEqual(response_implied_index.data, response_explicit_index.data)

    def test_build_search_path(self):
        search_path = self.app.build_search_path('/foo/bar/baz/index.html')        
        first_item_should_be = os.path.join(self.test_project,'foo/bar/baz/')

        self.assertEqual(first_item_should_be, search_path[0])
        self.assertEqual(self.test_project, os.path.normpath(search_path[-1]))
        
    def test_add_slash(self):
        response = self.client.get('/foo')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertEqual(response.headers['Location'], "http://localhost/foo/")



class TestWSGIWithAltURL(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        self.test_project = os.path.join(module_path, 'testproject')

        self.app = shortstack.wsgi.Shortstack('shortstack', instance_path=self.test_project,
                                              url_root='/about-us/')
        self.client = Client(self.app, BaseResponse)

    def test_redirect_to_url_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertEqual(response.headers['Location'], "http://localhost/about-us/")


    def test_not_redirecting_for_url_in_root(self):
        response = self.client.get('/about-us/index.html')
        self.assertEqual(response.status_code, 200)
