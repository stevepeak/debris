class Memory:
    STOCKPILE = {}
    @classmethod
    def get(self, namespace):
        return self.STOCKPILE.get(namespace, None)

    @classmethod
    def set(self, namespace, obj):
        self.STOCKPILE[namespace] = obj
