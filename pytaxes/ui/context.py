from itertools import chain

class ContextManager(object):
    """Produces dicts for the responces"""
    def __init__(self, **kw):
        self.temp = {}
        self.perm = kw

    def __getitem__(self, key):
        if key in self.temp:
            return self.temp[key]
        try:
            return self.perm[key]
        except KeyError:
            return None

    def __setitem__(self, key, v):
        self.permanent((key,v))

    def temporary(self, (k, v)):
        self.temp[k] = v

    def permanent(self, (k,v)):
        self.perm[k] = v

    def messages_update(self, ht):
        """Update errors, info and successes based on a hash table"""
        for i in ht.extract_messages().iteritems():
            self.temporary(i)

    def __call__(self, **kw):
        ret = dict((k,v) for k,v in chain(self.perm.iteritems(), self.temp.iteritems(), kw.iteritems()))
        self.temp = {}
        return ret
