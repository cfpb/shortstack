"""Functions related to filesystem access"""

import os
import os.path
import functools

from .url_manipulation import prepend_url


def relative_urls_from_filesystem(root_dir, prepend_path):
    for dirpath, dirnames, filenames in os.walk(root_dir):

        complete_path_joiner = functools.partial(os.path.join, dirpath)
        complete_paths = map(complete_path_joiner, filenames)
        for path in complete_paths:
            yield prepend_url(prepend_path, '/' + os.path.relpath(path, root_dir))
