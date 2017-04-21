'''
stores the basic class
'''


class BrowserBase(object):
    '''base object to make init easier'''
    def __init__(self, rng=None):
        pass

    def _init(self, local):
        '''helper method for subclasses to initialize itself'''

        for key, val in local.iteritems():
            if key not in ['self', 'rng']:
                setattr(self, key, val)
