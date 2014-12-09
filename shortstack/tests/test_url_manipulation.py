try:
    import unittest2 as unittest
except ImportError:
    import unittest

from shortstack import url_manipulation


class TestPathInPatterns(unittest.TestCase):

    def test_path_in_patterns(self):
        patterns = ['_foo/*', '.git', 'blue/red']
        self.assertTrue(url_manipulation.path_in_patterns(patterns, "_foo/bar.txt"))
