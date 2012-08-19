from datetime import date, timedelta

class Card(dict):
    """A card able to match stuff on it's own."""

    def __init__(self, string=None, **kw):
        """No security is enforced at this point. You can have any
        field your heart desires. This will break on the way though"""
        if string:
            self.parse_string(string)
        super(Card, self).__init__(kw)


    def parse_string(self, string):
        it = iter(string.split(";"))
        self['id'] =  it.next()
        year = int(it.next())
        days = int(it.next())
        self['cost'] = it.next()
        self['vendor'] = it.next()
        self['products'] = [i for i in it]
        self['date'] = date(year, 1, 1) + timedelta(days-1)

    def matches(self, (k,v)):
        """Check if the tuple matches any my values"""
        if k not in self:
            return False

        if k == 'date':
            try:
                # date range
                return self['date'] in v
            except TypeError:
                return v == self['date']

        if k == 'product' or k == 'products':
            return v in self['products']

        return self[k] == v
