import os

class PostgreSQL(object):
    def __init__(self, url=None):
        try:
            import tornpsql
        except ImportError:
            self._bank = None
        else:
            self._bank = tornpsql.Connection(url or os.getenv("PSQL"))

    def get(self, query, **kwargs):
        return self._bank.get(query, **kwargs)

    def getmany(self, query, **kwargs):
        return self._bank.query(query, **kwargs)
