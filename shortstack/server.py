from .wsgi import Shortstack


def start(args, config):
    location = config['location']
    debug = config['debug']
    application = Shortstack('shortstack',
                             instance_path=location)

    if debug:
        application.debug = True

    application.run(host=args.addr, port=int(args.port))
