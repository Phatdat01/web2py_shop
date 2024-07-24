def index():
    return dict(message="Hello from user shop")

def data():
    rows = db(db.user_shop).select()
    return locals()

def count_user():
    num = db(db.user_shop).count()
    return locals()

def done():
    return locals()

@auth.requires_membership('create_user')
def post():
    form = SQLFORM(db.user_shop)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('done'))
    elif form.errors:
        response.flash = 'input errors'
    else:
        response.flash = "please fill"    
    return locals()

def update():
    record = db.user_shop(request.args(0) or redirect(URL('post')))
    form = SQLFORM(db.user_shop, record)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('done'))
    elif form.errors:
        response.flash = 'input errors'
    else:
        response.flash = "please fill"    
    return locals()

def view():
    rows = db(db.user_shop).select(orderby=~db.user_shop.id)
    return locals()