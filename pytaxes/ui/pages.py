class PageManager(object):
    def __init__(self, parser, hash_table, current=0):
        self.cards = parser.search(hash_table)
        self.current = current

    @property
    def pages(self):
        groups = [iter(self.cards)]*CARDS_PER_PAGE
        return [Page(cl, n) for n,cl in enumerate(groups)]

    @property
    def page(self):
        return self.pages[self.current]

    @property
    def prev(self):
        if 0 <= self.current-1 < len(self.pages):
            return self.pages[self.current-1]
        else:
            return None

    @property
    def next(self):
        if 0 <= self.current+1 < len(self.pages):
            return self.pages[self.current+1]
        else:
            return None

class Page(object):
    def __init__(self, cards, number):
        self.cards = cards
        self.number = number

    @property
    def cards(self):
        return self.cards

    @property
    def n(self):
        return self.number
