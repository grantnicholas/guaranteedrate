class DataFetcher:
    """
    Let's model our database with a simple in memory list
    """
    def __init__(self):
        self._DATABASE = []

    def insert_records(self, recs):
        self._DATABASE.extend(recs)

    def get_records(self):
        return self._DATABASE

    def clear_records(self):
        self._DATABASE = []
