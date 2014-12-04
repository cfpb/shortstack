import os.path
import functools

import six
import flask


def path_ancestors(path):
    stop_search_at_char = 10000
    path = path.lstrip('/')
    ancestors = []

    while stop_search_at_char > 0:
        next_ancestor_end = path.rfind('/', 0, stop_search_at_char)
        ancestors.append(path[0:next_ancestor_end + 1])
        stop_search_at_char = next_ancestor_end

    return ancestors


def build_search_path(instance_path, seeking_path, append=None, include_start_directory=True):
    rel_search_path = []

    rel_search_path += path_ancestors(seeking_path)

    if append and type(append) in (str, six.text_type):
        append_paths = [append]
    elif append:
        append_paths = append
    else:
        append_paths = []

    naked_paths = [os.path.join(instance_path, p) for p in rel_search_path]

    search_path = []

    for path in naked_paths:
        if include_start_directory:
            search_path.append(path)

        for extra_path in append_paths:
            extended_path = os.path.join(path, extra_path)
            search_path.append(extended_path)

    return search_path


def build_search_path_for_request(request,
                                  seeking_path,
                                  append=None,
                                  include_start_directory=False):
    instance_path = flask.current_app.instance_path

    return build_search_path(instance_path, seeking_path, append=append, include_start_directory=include_start_directory)


def find_in_search_path(filename, paths):
    possible_paths = (os.path.join(p, filename) for p in paths)
    paths_that_exist = (p for p in possible_paths if os.path.exists(p))
    return next(paths_that_exist)
