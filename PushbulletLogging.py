#!/usr/bin/env python3
# coding=utf-8

from logging import Handler
from logging import LogRecord
from logging import Formatter
from logging import Logger

try:
    import json
except ImportError:
    import simplejson

try:
    import http.client as client
except ImportError:
    import httplib as client


class PushbulletHandlerTarget(object):

    def params(self):
        raise NotImplementedError("Please Implement this method")


class PushbulletHandlerMailTarget(PushbulletHandlerTarget):

    def __init__(self, address):
        assert isinstance(address, basestring)
        self.address = address

    def params(self):
        return {'email': self.address}


class PushbulletHandlerChannelTarget(PushbulletHandlerTarget):

    def __init__(self, channel_tag):
        assert isinstance(channel_tag, basestring)
        self.channel_tag = channel_tag

    def params(self):
        return {'channel_tag': self.channel_tag}


class PushbulletHandler(Handler):

    def __init__(self,
                 access_token,
                 target=None,
                 title_format=Formatter('%(levelname)s %(name)s'),
                 body_format=Formatter('%(msg)s')):

        assert isinstance(access_token, basestring)
        assert isinstance(target, PushbulletHandlerTarget) or callable(target) or target is None
        assert isinstance(title_format, Formatter)
        assert isinstance(body_format, Formatter)

        self.access_token = access_token
        self.target = target
        self.title_format = title_format
        self.body_format = body_format

        super(PushbulletHandler, self).__init__()

    def emit(self, record):
        """
        Emit the push.

        :param record: instance of logging.LogRecord
        """
        try:

            assert isinstance(record, LogRecord)
            params = {
                "type": "note",
                "title": self.title_format.format(record),
                "body": self.body_format.format(record)
            }

            if self.target:
                if callable(self.target):
                    target = self.target(record)
                else:
                    target = self.target

                if isinstance(target, PushbulletHandlerTarget):
                    params.update(target.params())

            data = json.dumps(params)
            c = client.HTTPSConnection('api.pushbullet.com')
            c.putrequest('POST', '/v2/pushes')
            c.putheader("Host", 'api.pushbullet.com')
            c.putheader("Content-type", "application/json")
            c.putheader("Content-length", str(len(data)))
            c.putheader('Authorization', 'Bearer %s' % self.access_token)
            c.endheaders()
            c.send(data.encode('utf-8'))
            c.getresponse()

        except http.client.HTTPException:
            self.handleError(record)
