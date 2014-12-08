"""Functions related to filesystem access"""

import os
import os.path
import fnmatch
import functools


def ignore_match(patterns, path):
    pattern_matches = (
        pattern for pattern in patterns if fnmatch.fnmatch(path, str(pattern)))
    return any(pattern_matches)


def relative_urls_from_filesystem(root_dir, prepend_path):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        complete_path_joiner = functools.partial(os.path.join, dirpath)
        complete_paths = map(complete_path_joiner, filenames)
        for path in complete_paths:
            yield prepend_path+os.path.relpath(path, root_dir)
