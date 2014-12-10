import itertools

import flask
from jinja2.loaders import FileSystemLoader

from .views import handle_request
from .filesystem import relative_urls_from_filesystem
from .url_manipulation import path_in_patterns, prepend_url
from .utility import build_search_path


DEFAULT_IGNORE = ['_layouts/*', '_settings/*']


class Shortstack(flask.Flask):

    def __init__(self, *args, **kwargs):
        self.url_root = kwargs.pop('url_root', '/')
        assert self.url_root.startswith('/'), "url_root must start with slash"
        assert self.url_root.endswith('/'), "url_root must end with slash"

        # This helps us take the url_root into account
        # when translating URL paths to the filesystem
        self.trim_from_paths = len(self.url_root) - 1

        super(Shortstack, self).__init__(*args, **kwargs)

        template_search_path = [self.join_path('_layouts'),
                                self.join_path('_includes')]

        self.jinja_loader = FileSystemLoader(template_search_path)

        try:
            with self.open_instance_resource('.ssignore') as ignorefile:
                self.ignore_patterns = [l.strip() for l in ignorefile]
        except IOError:
            self.ignore_patterns = []

        @self.errorhandler(404)
        def _(e):
            return handle_request()

    def should_ignore_path(self, path):
        ignore_patterns = itertools.chain(DEFAULT_IGNORE, self.ignore_patterns)
        stripped_path = path[self.trim_from_paths + 1:]
        return path_in_patterns(ignore_patterns, stripped_path)

    def filtered_urls_from_filesystem(self):
        unfiltered = relative_urls_from_filesystem(
            self.instance_path, self.url_root)
        return (url for url in unfiltered if not self.should_ignore_path(url))

    def join_path(self, relative_path):
        if relative_path.startswith('/'):
            relative_path = relative_path[1:]
        return flask.safe_join(self.instance_path, relative_path)

    def trim_path(self, path):
        if path.startswith(self.url_root):
            return path[self.trim_from_paths:]
        else:
            return path

    def filesystem_path_for_request(self):
        trimmed = self.trim_path(flask.request.path)

        if trimmed.endswith('/'):
            trimmed += ('index.html')

        translated_path = self.join_path(trimmed)
        return translated_path

    def build_search_path(self, *args, **kwargs):
        return build_search_path(self.instance_path, *args, **kwargs)

    def dispatch_request(self):
        prepared_url = prepend_url(self.url_root,flask.request.path)
        if prepared_url != flask.request.path:
            return flask.redirect(prepared_url)
        super(Shortstack, self).dispatch_request()
