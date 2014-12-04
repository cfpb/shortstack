import shortstack.routing

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestRouting(unittest.TestCase):

    def setUp(self):

        self.rule = shortstack.routing.SSRule('/agents/<name>.html',
                                              callable=type)

        self.ssmap = shortstack.routing.SSMap([self.rule])

    def test_rule_match(self):
        rule, data = next(self.ssmap.multimatch('/agents/coulson.html'))
        self.assertIn('name', data)

    def test_no_match(self):
        with self.assertRaises(StopIteration):
            rule, data = next(self.ssmap.multimatch('/avengers/thor.html'))
