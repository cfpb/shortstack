from werkzeug.routing import Rule, DEFAULT_CONVERTERS


class SSRule(Rule):
    """
    Rule subclass that adds an attribute for an attched callable.
    """
    def __init__(self, *args, **kwargs):
        self.callable = kwargs.get('callable')
        if self.callable:
            del kwargs['callable']
        super(SSRule, self).__init__(*args, **kwargs)


class SSMap(object):
    """
    Pretends to be a werkzeug.routing.map, and provides a 'multimatch'
    method that returns ALL matching rules (and their results).
    """

    strict_slashes = True
    default_subdomain = None
    host_matching = False
    converters = DEFAULT_CONVERTERS
    rules = []

    def __init__(self, rules):
        for rule in rules:
            rule.bind(self)
            self.rules.append(rule)

    def multimatch(self, path):
        lookup = "|%s" % path
        matches = [(rule, rule.match(lookup)) for rule in self.rules]
        successful_matches = ((r, m) for r, m in matches if m is not None)
        return successful_matches
