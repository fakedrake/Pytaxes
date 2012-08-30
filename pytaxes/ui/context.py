class ContextManager(object):
    """Produces dicts for the responces"""
    def __init__(self, **kw):
        self.temp = []
        self.data = kw

    def temporary(self, (k, v)):
        if k not in self.temp:
            self.temp += k
        self.data[k] = v

    def permanent(self, (k,v)):
        self.data[k] = v

    def __call__(self, **kw):
        return {k:v for k,v in chain(self.data.iteritems(), kw.iteritems())}
