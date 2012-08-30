import os
import logging

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.httpexceptions import HTTPFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config

from wsgiref.simple_server import make_server

import sqlite3

logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))
env = ContextManager()

# views
@view_config(route_name='list', renderer='index.pt')
def list_view(request):
    if request.GET['search']:
        pages = PagesManager(hash_table=ht)
    else:
        pages = PagesManager(parser=Parser(request.GET["search"], hash_table=ht))
    return env(pages=pages)

@view_config(route_name='delete')
def list_view(request):
    if 'search' in request.GET:
        pages = PagesManager(hash_table=ht)
    else:
        pages = PagesManager(parser=Parser(request.GET["search"], hash_table=ht))
    return env(pages=pages)

if __name__ == '__main__':
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')
    settings['db'] = os.path.join(here, 'tasks.db')
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    # routes setup
    config.add_route('list', '/')
    config.add_route('new', '/new')
    config.add_route('close', '/close/{id}')
    # static view setup
    config.add_static_view('static', os.path.join(here, 'static'))
    # scan for @view_config and @subscriber decorators
    config.scan()
    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
