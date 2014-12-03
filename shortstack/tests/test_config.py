import os
import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from shortstack import config


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        self.test_project = os.path.join(module_path, 'testproject')
        self.test_config_directory = os.path.join(
            self.test_project, '_settings')

    def test_get_config_path(self):
        path = config.configuration_path('foo')
        self.assertEqual(path, '_settings/foo.json')

    def test_get_required_config(self):
        configuration = config.configuration('required',
                                             config_directory=self.test_config_directory)
        self.assertIn("foo", configuration)

    def test_missing_required_config(self):
        with self.assertRaises(config.ConfigMissing):
            config.configuration('missing',
                                 config_directory=self.test_config_directory)

    def test_missing_optional_config(self):
        configuration = config.configuration('missing',
                                             config_directory=self.test_config_directory,
                                             optional=True)
        self.assertIsInstance(configuration, dict)
