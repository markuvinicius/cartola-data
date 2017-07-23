class MyCache(object):

    def __init__(self):
        """Constructor"""
        self.cache = {}
        self.max_cache_size = 10

    def __init__(self,data):
        """Constructor"""
        self.cache = data
        self.max_cache_size = 10

    def __contains__(self, key):
        """
        Returns True or False depending on whether or not the key is in the
        cache
        """
        return key in self.cache

    def update(self, key, value):
        """
        Update the cache dictionary and optionally remove the oldest item
        """
        self.cache[key] = value

    def get_value(self,key):
        if key in self.cache:
            return self.cache[key]