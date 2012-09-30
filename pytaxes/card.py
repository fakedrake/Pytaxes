from datetime import date, timedelta

class Purchase(dict):
    """This isnt supposed to be used by the outer
    world. Create cards and they will keep their data in terms of
    purchases automatically."""

    def __init__(self, d):
        """Keep a copyof this dict"""
        for k,v in d.iteritems():
            self[k] = v

    def __hash__(self):
        return "%s:%s" % (self['id'], str(self['date']))

class Card(object):
    """A card able to match stuff on it's own."""

    def __init__(self, string=None, purchases=None, **kw):
        """No security is enforced at this point. You can have any
        field your heart desires. This will break on the way though"""
        if purchases:
            self.purchases = purchases
        else:
            self.purchases = []
            if string:
                self.purchases.append(Purchase(self.parse_string(string)))
            else:
                self.purchases.append(Purchase(kw))

        self._id = self.purchases[0]['id']

    def __hash__(self):
        """This has nothing to do with the hash table. The hashtable
        itself knows how to hash each card. This is so that i can
        insert cards in sets
        """
        return hash(self.id)

    @property
    def id(self):
        return self._id

    def __getitem__(self, it):
        if it == "cost":
            ret = 0
            for p in self.purchases:
                ret += p['cost']
            return ret

        if it == 'products':
            s =  set()
            for p in self.purchases:
                s = s.union(p['products'])
            return s

        # Return the first date
        return self.purchases[0][it]


    def parse_string(self, string):
        ret = dict()
        if string[-1] == "\n":
            string = string[:-1]

        it = iter(string.split(";"))
        ret['id'] =  it.next()
        year = int(it.next())
        days = int(it.next())
        ret['cost'] = float(it.next())
        ret['vendor'] = it.next()
        ret['products'] = set([i for i in it])
        ret['date'] = date(year, 1, 1) + timedelta(days)
        return ret

    def matches(self, (k,v)):
        """Return a version of yourself only with the interesting purchases
        """
        ret = []
        for p in self.purchases:
            if k not in p:
                return False

            if k == 'date' and v[0] <= p['date'] <= v[1]:
                ret.append(p)
                continue

            if (k == 'product' or k == 'products') and set(v) <= p['products']:
                ret.append(p)
                continue

            if p[k] == v:
                ret.append(p)
                continue
        if ret:
            return Card(purchases=ret)
        else:
            return None

    def purchase(self, card):
        """Copy the purchases of that card to this one."""
        self.purchases += card.purchases

    def __str__(self):
        return """<h4>%s</h4>
        <ul>
         <li>Date: %s</li>
         <li>Cost: %s</li>
         <li>Vendor: %s</li>
         <li>Products: %s</li>
        </ul>""" % \
    (self['id'], self['date'].strftime("%d/%m/%Y"), str(self['cost']), self['vendor'], str(self['products']))
