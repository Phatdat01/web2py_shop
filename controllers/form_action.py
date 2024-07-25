class FormAction:
    def __init__(self, db, session, response):
        self.db = db
        self.session = session
        self.response = response

    def insert(self, table):
        form = SQLFORM(table)
        if form.process().accepted:
            self.session.flash = 'form accepted'
            redirect(URL('done'))
        elif form.errors:
            self.response.flash = 'input errors'
        else:
            self.response.flash = "please fill"
        return form

    def index(self, table):
        rows = self.db(table).select()
        return rows