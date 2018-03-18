
class DictHash:
    def __init__(self):
        self._dict = {}

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        fund = False
        keys = self._dict.keys()
        for existingKey in keys:
            if existingKey == key:
                fund = True
        return fund

    def store(self, key, data):
        """sorterar in data i en hashtabell med nyckeln key"""
        self._dict[key] = data

    def search(self, key):
        """hitar data som tillhör nycken key"""
        return self._dict[key]


