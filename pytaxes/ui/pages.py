from ..search import Parser
from itertools import chain

CARDS_PER_PAGE = 10
VISIBLE_PAGES = 8

class PageManager(object):
    def __init__(self, search_string, hash_table, current=0, sort=None):
        self.parser = Parser(search_string)

        if sort:
            self.cards = sorted(self.parser.search(hash_table), key=lambda x: x['cost'], reverse=True)
        else:
            self.cards = self.parser.search(hash_table)

        if 0<=current<len(self.cards)/CARDS_PER_PAGE:
            self.current = current
        else:
            self.current = 0


    @property
    def page_links(self):
        if self.current-VISIBLE_PAGES/2 >= 0:
            first = self.current-VISIBLE_PAGES/2
        else:
            first = 0


        return self.pages[first:self.current+VISIBLE_PAGES/2]

    @property
    def pages(self):
        groups = [self.cards[i:i+CARDS_PER_PAGE] for i in range(0, len(self.cards), CARDS_PER_PAGE)]
        return [Page(cl, n, n==self.current) for n,cl in enumerate(groups)]

    @property
    def page(self):
        if self.pages:
            print "Opening results page", self.current,"/", len(self.pages)
            return self.pages[self.current]
        return Page([],0)

    @property
    def first(self):
        return pages[0]

    @property
    def last(self):
        return pages[-1]

class Page(object):
    """A page knows its place and it knows it's contents.'"""
    def __init__(self, cards, number, current=False):
        self._cards = cards
        self._number = number
        self.current = current

    @property
    def cards(self):
        return self._cards

    @property
    def n(self):
        return self._number

    @property
    def state(self):
        if self.current:
            return "active"
        return "clickable"

    def url(self, request):
        return request.route_url('list', _query=dict(i for i in chain(request.GET.iteritems(), {'p':self.n}.iteritems())))
