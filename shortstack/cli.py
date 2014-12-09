"""The shortstack command-line interface"""
import os.path

from argparse import ArgumentParser

import six

import shortstack.server
import shortstack.builder

LOCATION = os.environ.get('SS_LOCATION', os.getcwd())
URL_ROOT = os.environ.get('SS_URL_ROOT', '/')
DEBUG = bool(os.environ.get('SS_DEBUG', False))


def add_builder_subparser(subparsers):
    """
    Create the subparser for 'shorts build'
    """
    builder_parser = subparsers.add_parser('build',
                                           help="build a statuc HTML"
                                                "version of this"
                                                "project")

    builder_parser.set_defaults(func=shortstack.builder.build_static_site)

    builder_parser.add_argument('--destination', '-d', default='_build')
    builder_parser.add_argument('--really-delete', default=False,
                                help="delete existing built site")


def add_server_subparser(subparsers):
    """
    Create the subparser for 'shorts serve'
    """
    server_parser = subparsers.add_parser('serve',
                                          help="serve this site")

    server_parser.set_defaults(func=shortstack.server.start)

    server_parser.add_argument('--port', '-p',
                               default='7000',
                               help="port to run the web server on")

    server_parser.add_argument('--addr',
                               '-a',
                               default='0.0.0.0',
                               help="address to run the web server on")
    return server_parser


def apply_universal_arguments(subparser):
    """
    Add common arguments to all subparsers
    """
    subparser.add_argument(
        '--debug',
        help="print debugging output to the console",
        action='store_true', default=DEBUG)

    subparser.add_argument(
        '--location',
        '-l',
        default=LOCATION,
        help="Directory you want to operate on.")

    subparser.add_argument(
        '--url',
        '-u',
        default=URL_ROOT,
        help="url root for the files in this project")


def run_cli():
    """This is the command line interface to shortstack"""
    parser = ArgumentParser(prog='shorts',
                            description="Shortstack is an extensible"
                                        "site rendering system")

    subparsers = parser.add_subparsers()

    add_server_subparser(subparsers)
    add_builder_subparser(subparsers)

    for _, sub in six.iteritems(subparsers.choices):
        apply_universal_arguments(sub)

    arguments = parser.parse_args()

    if hasattr(arguments, 'func'):
        config = dict(debug=arguments.debug,
                      location=os.path.join(os.getcwd(), arguments.location),
                      url_root=arguments.url)
        arguments.func(arguments, config)
    else:
        parser.print_help()
