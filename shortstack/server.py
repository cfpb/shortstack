from .wsgi import Shortstack


def start(args, config):
    location = config['location']
    url_root = config['url_root']
    debug = config['debug']
    application = Shortstack('shortstack',
                             instance_path=location,
                             url_root=url_root)

    if debug:
        application.debug = True

    application.run(host=args.addr, port=int(args.port))
