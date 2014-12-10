import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import shortstack.wsgi
from shortstack import filesystem




class TestURLGeneration(unittest.TestCase):

    def test_urls_from_filesystem(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        test_project = os.path.join(module_path, 'testproject')

        app = shortstack.wsgi.Shortstack('shortstack', instance_path=test_project)
        url_generator = app.filtered_urls_from_filesystem()
        urls = [u for u in url_generator]
        self.assertIn('/style.css', urls)
