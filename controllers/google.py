from gluon.tools import Auth

def index():
    auth = Auth(db)
    auth.define_tables(username=False, signature=False)

    return locals()