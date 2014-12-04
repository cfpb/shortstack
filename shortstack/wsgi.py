import flask
from jinja2.loaders import FileSystemLoader
from werkzeug.routing import RequestRedirect

from .views import handle_request
from .utility import build_search_path


class Shortstack(flask.Flask):

    def __init__(self, *args, **kwargs):
        super(Shortstack, self).__init__(*args, **kwargs)

        template_search_path = [self.join_path('_layouts'),
                                self.join_path('_includes')]

        self.jinja_loader = FileSystemLoader(template_search_path)

        @self.errorhandler(404)
        def _(e):
            return handle_request()

    def join_path(self, relative_path):
        if relative_path.startswith('/'):
            relative_path = relative_path[1:]
        return flask.safe_join(self.instance_path, relative_path)

    def filesystem_path_for_request(self):
        raw_path = flask.request.path
        if raw_path.endswith('/'):
            raw_path += ('index.html')

        translated_path = self.join_path(raw_path)
        return translated_path

    def build_search_path(self, *args, **kwargs):
        return build_search_path(self.instance_path, *args, **kwargs)

    def dispatch_request(self):
        try:
            flask_response = super(Shortstack, self).dispatch_request()
            return flask_response

        except RequestRedirect:

            filesystem_path = self.filesystem_path_for_request()
            if os.path.isfile(filesystem_path):
                return handle_request()
            raise
