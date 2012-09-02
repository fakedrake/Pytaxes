import os
import logging

from itertools import chain

from .context import ContextManager
from .pages import PageManager

from ..hashtable import HashTable, index_file
from ..card import Card

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from context import ContextManager

from wsgiref.simple_server import make_server

logging.basicConfig()
log = logging.getLogger(__file__)


HELP_TEXT = """The search bar is more than it seems you can type 'help' for this
message, 'ADD <card ; separated representation>' to add a card, 'DEL
<card id>' to delete a card, 'stats' for colision count in hash table,
'toggle duplicate silence' to show an error when a duplicate card is
added."""
ADD_CARD = ['ADD']
DELETE_CARD = ["DEL"]
STATS = ["conflicts", "stats", "Stats", "STATS"]
HELP = ["h", 'help', 'HELP', 'info']
TOGGLE_DUPLICATE_SILENCE = ["toggle duplicate silence"]

here = os.path.dirname(os.path.abspath(__file__))
env = ContextManager(errors=[], warnings=[], successes=[], infos=[], ht=HashTable(), duplicate_silence=True)

def command(c):
    """Cascade the search term through here to execute any needed commands or pass throug if none are found"""
    if len(c.strip().split()) < 1:
        return c

    cmd = c.strip().split()[0]
    if cmd in HELP:
        env['ht'].infos.append(HELP_TEXT)


    if cmd in STATS:
        env['ht'].infos.append("The current table faced %d conflicts." % env['ht'].conflicts)
        return ""

    if len(c.strip().split()) < 2:
        return c

    arg = c.strip().split()[1]
    if cmd in ADD_CARD:
        env['ht'].insert(Card(arg))
        return "id %s" % arg.split(';')[0]

    if cmd in DELETE_CARD:
        env['ht'].delete(arg)
        return ""

    if c in TOGGLE_DUPLICATE_SILENCE:
        if env['duplicate_silence']:
            set_val = False
            str = " no more"
        else:
            set_val = True
            str = ""
        env.permanent(('duplicate_silence', set_val))
        env['ht'].duplicate_silence = set_val
        env['ht'].infos.append("Duplicates are silent%s" % str)
        return ""

    return c


# views
@view_config(route_name='delete')
def delete(request):
    env['ht'].delete(request.matchdict['id'])
    return HTTPFound(location=request.route_url('list'))


@view_config(route_name='upload')
def upload_file(request):
    if 'uploaded' in request.POST:
        file = request.POST['uploaded'].file
        env['ht'] = index_file("", file, duplicate_silence=env['duplicate_silence'])
    return HTTPFound(location=request.route_url('list'))


@view_config(route_name='list', renderer='index.pt')
def list_view(request):
    if 'p' in request.GET:
        current_page = int(request.GET['p'])
    else:
        current_page = 0

    if  'search' in request.GET:
        search = command(request.GET['search'])
        pages = PageManager(search, env['ht'], current_page)
    else:
        pages = PageManager("", env['ht'], current_page)

    env.messages_update(env['ht'])
    return env(pages=pages)


def main():
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')
    settings['db'] = os.path.join(here, 'tasks.db')
    # configuration setup
    config = Configurator(settings=settings)
    # routes setup
    config.add_route('delete', '/{id}/delete')
    config.add_route('upload', '/upload')
    config.add_route('list', '/')
    # static view setup
    config.add_static_view('static', os.path.join(here, 'static'))

    # scan for @view_config and @subscriber decorators
    config.scan()

    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)

    print "Almost there..."
    server.serve_forever()


if __name__ == '__main__':
    main()
