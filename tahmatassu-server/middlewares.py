"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
HTTP-status codes containing module
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""
from werkzeug.wsgi import LimitedStream

class StreamConsumingMiddleware(object):

  def __init__(self, app):
      self.app = app

  def __call__(self, environ, start_response):
    content_length = environ.get('CONTENT_LENGTH',0)
    content_length = 0 if content_length is '' else content_length

    stream = LimitedStream(environ.get('wsgi.input'),
                            int(content_length))
    environ['wsgi.input'] = stream
    app_iter = self.app(environ, start_response)
    try:
      stream.exhaust()
      for event in app_iter:
        yield event
    finally:
      if hasattr(app_iter, 'close'):
        app_iter.close()