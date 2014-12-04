import os

from shortstack.utility import build_search_path, find_in_search_path

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSearchPaths(unittest.TestCase):

    def test_simple_searchpath(self):
        paths = build_search_path('/var/sheer', '/my/site/is/cool/index.html')
        assert('/var/sheer/my/site/is/cool/' in paths)
        assert('/var/sheer/my/site/is/' in paths)
        assert('/var/sheer/my/site/' in paths)
        assert('/var/sheer/my/' in paths)
        assert('/var/sheer/' in paths)
        assert('/var/' not in paths)

    def test_searchpath_with_append(self):
        paths = build_search_path(
            '/var/sheer', '/my/site/is/cool/foo.html', append='_layouts', include_start_directory=False)
        assert('/var/sheer/my/site/_layouts' in paths)
        assert('/var/sheer/my/_layouts' in paths)
        assert('/var/sheer/_layouts' in paths)
        assert('/var/_layouts' not in paths)
        assert paths[0] == '/var/sheer/my/site/is/cool/_layouts'

    def test_searchpath_with_append_including_start(self):
        paths = build_search_path('/var/sheer',
                                  '/my/site/is/cool/foo.html',
                                  append='_layouts',
                                  include_start_directory=True)

        assert('/var/sheer/my/site/is/cool/_layouts' in paths)
        assert('/var/sheer/my/site/_layouts' in paths)
        assert('/var/sheer/my/_layouts' in paths)
        assert('/var/sheer/_layouts' in paths)
        assert('/var/_layouts' not in paths)
        assert paths[0] == '/var/sheer/my/site/is/cool/'

    def test_find_in_search_path(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        test_project = os.path.join(module_path, 'testproject')
        paths = build_search_path(test_project, '/foo/bar/missing.html')
        expected = os.path.join(test_project, 'foo/404.html')
        found = find_in_search_path('404.html', paths)
        self.assertEqual(expected, found)
