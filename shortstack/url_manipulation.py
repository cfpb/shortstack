import fnmatch

DEFAULT_NORELOCATE = ['/static/*']


def path_in_patterns(patterns, path):
    """Check a path against many fnmatch patterns"""
    pattern_matches = (
        pattern for pattern in patterns if fnmatch.fnmatch(path, str(pattern)))
    return any(pattern_matches)


def prepend_url(prepend, path, ignore_patterns=DEFAULT_NORELOCATE):
    if path.startswith(prepend) or path_in_patterns(ignore_patterns, path):
        return path
    elif path == '/':
        return prepend
    else:
        return prepend + path[1:]
