import os
import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import flask

import shortstack.views
import shortstack.wsgi


class TestView(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        self.test_project = os.path.join(module_path, 'testproject')

        self.app = shortstack.wsgi.Shortstack('shortstack', instance_path=self.test_project)

    def test_static_file(self):
        with self.app.test_request_context('/style.css'):
            self.app.preprocess_request()
            response = flask.make_response(shortstack.views.handle_request())
            self.assertEquals(response.status_code,200)

    def test_missing_file(self):
        with self.app.test_request_context('/foo/bar/index.html'):
            self.app.preprocess_request()
            response = shortstack.views.handle_request()
            self.assertEquals(response.status_code,404)

    def test_missing_404(self):
        with self.app.test_request_context('/i-aint-even-Bill-Nye.docx'):
            self.app.preprocess_request()
            response = flask.make_response(shortstack.views.handle_request())
            self.assertEquals(response.status_code,404)
