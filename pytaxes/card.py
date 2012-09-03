from datetime import date, timedelta

class Card(dict):
    """A card able to match stuff on it's own."""

    def __init__(self, string=None, **kw):
        """No security is enforced at this point. You can have any
        field your heart desires. This will break on the way though"""
        if string:
            self.parse_string(string)
        super(Card, self).__init__(kw)

    def __hash__(self):
        """This has nothing to do with the hash table. The hashtable
        itself knows how to hash each card. This is so that i can
        insert cards in sets
        """
        return hash(self['id'])

    def parse_string(self, string):
        if string[-1] == "\n":
            string = string[:-1]

        it = iter(string.split(";"))
        self['id'] =  it.next()
        year = int(it.next())
        days = int(it.next())
        self['cost'] = float(it.next())
        self['vendor'] = it.next()
        self['products'] = set([i for i in it])
        self['date'] = date(year, 1, 1) + timedelta(days-1)

    def matches(self, (k,v)):
        """Check if the tuple matches any my values. Dates must be
        tuples that represent inclusive ranges, costs must be integers
        and products are a list that matches if is a subset of our
        products.
        """
        if k not in self:
            return False

        if k == 'date':
            return v[0] <= self['date'] <= v[1]

        if k == 'product' or k == 'products':
            return set(v) <= self['products']

        # XXX: soon costs will be ranges too
        return self[k] == v

    def __str__(self):
        return "<h4>%s</h4><ul><li>Date: %s</li><li>Cost: %s</li><li>Vendor: %s</li><li>Products: %s</li></ul>" % \
          (self['id'], self['date'].strftime("%d/%m/%Y"), str(self['cost']), self['vendor'], str(self['products']))
