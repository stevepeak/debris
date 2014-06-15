import tornpsql


class PostgreSQL(object):
    """PostgreSQL plugin via stevepeak/tornpsql
    """
    def __init__(self, config):
        if config.get('url'):
            self.service = tornpsql.Connection(config.get("url"))
        elif config.get('connection'):
            self.service = config.get('connection')
        else:
            self.service = tornpsql.Connection()

    def get(self, query, **kwargs):
        result = self.service.get(query, **kwargs)
        if '__debris__' in result:
            result.update(result.pop("__debris__"))
        return result

    def getmany(self, query, **kwargs):
        results = self.service.query(query, **kwargs)
        for row in results:
            if '__debris__' in row:
                row.update(row.pop("__debris__"))
        return results
