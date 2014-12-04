"""The shortstack command-line interface"""
import os.path

from argparse import ArgumentParser

import shortstack.server

LOCATION = os.environ.get('SS_LOCATION', os.getcwd())
URL_ROOT = os.environ.get('SS_URL_ROOT', '/')
DEBUG = bool(os.environ.get('SS_DEBUG', False))


def run_cli():
    """This is a placeholder for the shortstack cli"""
    parser = ArgumentParser(prog='shorts',
                            description="Shortstack is an extensible"
                                        "site rendering system")

    subparsers = parser.add_subparsers()

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

    for p in [server_parser]:
        p.add_argument(
            '--debug',
            help="print debugging output to the console",
            action='store_true', default=DEBUG)

        p.add_argument(
            '--location',
            '-l',
            default=LOCATION,
            help="Directory you want to operate on.")

        p.add_argument(
            '--url',
            '-u',
            default=URL_ROOT,
            help="ROOT URL for the files in this project")

    args = parser.parse_args()

    config = dict(debug=args.debug,
                  location=os.path.join(os.getcwd(), args.location),
                  root_url=args.url
                  )
    args.func(args, config)
