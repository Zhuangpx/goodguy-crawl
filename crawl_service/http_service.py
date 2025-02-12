import json

from flask import Flask, request, abort
from gevent import pywsgi
from google.protobuf.json_format import Parse, MessageToJson

from crawl_service.crawl_service_impl import Interface, INTERFACES
from crawl_service.util.config import Config

APP = Flask(__name__)

__all__ = ['serve']


def decorator(interface: Interface):
    def wrapper():
        body = request.get_data()
        try:
            message = Parse(body, interface.message_type())
        except Exception as e:
            abort(400)
            _ = e
        else:
            return json.loads(MessageToJson(interface.handler(message), indent=0))

    wrapper.__name__ = interface.handler.__name__
    return wrapper


def serve():
    for interface in INTERFACES:
        APP.route(f'/{interface.handler.__name__}', methods=['POST'])(decorator(interface))
    host = Config.get("service.http.host", '0.0.0.0')
    port = Config.get("service.http.port", 50049)
    server = pywsgi.WSGIServer((host, port), APP)
    print('http crawl service is serving on 0.0.0.0:50049')
    server.serve_forever()


if __name__ == '__main__':
    serve()
