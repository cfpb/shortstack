"""
Static site generation for Shortstack
"""
from __future__ import print_function

import os
import shutil

from six.moves import input as six_input

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from .wsgi import Shortstack


def create_directories_if_needed(path):
    """
    create intermediate directories to the given path
    """
    dirname = os.path.dirname(path)
    try:
        os.makedirs(dirname)
    except OSError as err:
        # if the directory exists, errno will be 17
        if err.errno != 17:
            raise


def save_document(client, destination_dir, path):
    """
    Use the passed werkzeug.test Client to
    save a given URL path to the destination_dir
    """
    response = client.get(path)

    save_filename = os.path.join(destination_dir, path[1:])
    create_directories_if_needed(save_filename)

    with open(save_filename, "wb") as destination:
        destination.write(response.get_data())


def build_static_site(arguments, config):
    """
    Do the actual work of building a static site
    """
    # create Shortstack instance
    location = config['location']
    url_root = config['url_root']
    destination = arguments.destination

    application = Shortstack('shortstack',
                             instance_path=location,
                             url_root=url_root)

    client = Client(application, BaseResponse)
    print("Generating static site at: %s" % destination)
    if os.path.exists(destination):
        prompt = "Really delete (and rebuild) %s ? [y/n] " % destination
        really_delete = six_input(prompt).lower() == 'y'
        if really_delete:
            shutil.rmtree(arguments.destination)
        else:
            return
    for url in application.filtered_urls_from_filesystem():
        save_document(client, arguments.destination, url)
