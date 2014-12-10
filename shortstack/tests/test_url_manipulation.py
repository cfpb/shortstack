try:
    import unittest2 as unittest
except ImportError:
    import unittest

from shortstack import url_manipulation


class TestPathInPatterns(unittest.TestCase):

    def test_path_in_patterns(self):
        patterns = ['_foo/*', '.git', 'blue/red']
        self.assertTrue(url_manipulation.path_in_patterns(patterns, "_foo/bar.txt"))


class TestPathPrepender(unittest.TestCase):

    def test_prepend_url(self):
        norelocate_patterns = ['/static/*']
        url_root = '/my-homepage/'
        test_cases = (('/static/main.css', '/static/main.css'),
                      ('/my-homepage/index.html', '/my-homepage/index.html'),
                      ('/index.html', '/my-homepage/index.html'))

        for input, expected in test_cases:
            output = url_manipulation.prepend_url(url_root,
                                                  input,
                                                  norelocate_patterns)
            self.assertEqual(output, expected)
