import os.path
import codecs
import mimetypes

import flask
from flask import request
from werkzeug.exceptions import HTTPException, NotFound

from .utility import build_search_path, build_search_path_for_request, find_in_search_path


def handle_request():
    app = flask.current_app
    translated_path = app.filesystem_path_for_request()

    if os.path.isdir(translated_path) and not flask.request.path.endswith('/'):
            return flask.redirect(flask.request.path + '/')

    if not translated_path.endswith('.html') and os.path.exists(translated_path):
        mime, encoding = mimetypes.guess_type(translated_path)

        return flask.send_file(translated_path), 200, {'Content-Type': mime}

    template_candidates = [translated_path]

    try:

        template_path = next(
            t for t in template_candidates if os.path.isfile(t))

        if os.path.exists(template_path):
            template_context = {}

            with codecs.open(template_path, encoding="utf-8") as template_source:
                return flask.make_response(flask.render_template_string(template_source.read(), **template_context),200)

    except StopIteration:
        return serve_error_page(404)


def serve_error_page(error_code):
    request = flask.request
    app = flask.current_app

    # TODO: this seems silly
    # We shouldn't even need to send the request object,
    # and the second argument should usually be request.path anyways

    trimmed_path = app.trim_path(request.path)
    search_path = build_search_path_for_request(
        request, trimmed_path, append=['_layouts', '_includes'], include_start_directory=True)


    try:
        template_path = find_in_search_path('%s.html' % error_code, search_path)

        with codecs.open(template_path, encoding="utf-8") as template_source:
            return flask.make_response(flask.render_template_string(template_source.read()), error_code)

    except StopIteration:
        return "Please provide a %s.html!" % error_code, error_code
