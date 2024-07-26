class FormAction:
    def __init__(self, db, session, response):
        self.db = db
        self.session = session
        self.response = response

    def index(self, table):
        rows = self.db(table).select()
        return rows