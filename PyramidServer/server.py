from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import logging
import SentimentAnalyzer

my_logger = logging.getLogger()
my_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename='sample.log')

@view_config(
    route_name='home',
    renderer='templates/index.jinja2'
)
def home(request):
    return {"Status": 'Ok'}


@view_config(route_name='check',renderer='string')
def check(request):
    review = request.POST['data']
    result = SentimentAnalyzer.predictOutput(review)
    return result

#Uncomment to allow CORS
def request_factory(environ):
    request = Request(environ)
    if request.is_xhr:
        request.response = Response()
        request.response.headerlist = []
        request.response.headerlist.extend(
            (
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'application/json')
            )
        )
    return request

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_route('home', '/')
        config.add_route('check', '/check')
        #Uncomment to allow CORS
        # config.set_request_factory(request_factory)
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    server.serve_forever()