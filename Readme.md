### Python logging.handler for Pushbullet

This is a simple logging.handler to send log messages as pushes via [Pushbullet](https://www.pushbullet.com/). To use it, you will need an account and the access_token, which can be found in the account settings.

#### Usage:

The most simple case is:

    import logging
    from PushbulletLogging import PushbulletHandler

    logger = logging.getLogger('My Application')
    logger.addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN'))
    logger.error('This is an example.')

It is also possible to define a push target like this:

    from PushbulletLogging import PushbulletHandlerMailTarget
    logger.addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN',
                                        target=PushbulletHandlerMailTarget('user@example.com')))

    from PushbulletLogging import PushbulletHandlerChannelTarget
    logger.addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN',
                                        target=PushbulletHandlerChannelTarget('channeltag')))

The target can also be a callable, that returns the target. This allows you to push to different targets, dependent e.g. on the current time or weather.

    import time
    from PushbulletLogging import PushbulletHandlerMailTarget

    def callable_target(record):
        utc_hour = int(time.time() / (60*60) % 24)
        if 8 < utc_hour < 20:
            return PushbulletHandlerMailTarget('user@example.com')
        else:
            return PushbulletHandlerMailTarget('admin@example.com')

    logger.addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN', target=callable_target))

The handler also allows to set a formatter to define the content of the title an the body. Here you can use basically all elements from the [logging.LogRecord Objects](https://docs.python.org/3/library/logging.html#logrecord-objects).

    from PushbulletLogging import PushbulletHandler
    from logging import Formatter

    logger.addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN',
                                        title_format=Formatter('%(name)s'),
                                        body_format=Formatter('%(levelname)s %(msg)s')))

To use the root logger:

    import logging
    from PushbulletLogging import PushbulletHandler

    logging.getLogger().addHandler(PushbulletHandler(access_token='YOUR_ACCESS_TOKEN'))
    logging.error('This is an example.')

My use case: Log interesting messages to the log file, but also push urgent ones to my devices.

    import logging
    from PushbulletLogging import PushbulletHandler
    
    pushbullet_handler = PushbulletHandler(access_token='YOUR_ACCESS_TOKEN')
    pushbullet_handler.setLevel(logging.CRITICAL)
    logging.getLogger().addHandler(pushbullet_handler)
    
    log_file_handler = logging.FileHandler('application.log')
    log_file_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(log_file_handler)
    
    logging.debug('This message is thrown away.')
    logging.error('This message gets only to the logfile.')
    logging.critical('This message is pushed and gets to the logfile.')

