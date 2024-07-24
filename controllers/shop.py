def index():
    return dict(message="Hello from shop")

@auth.requires_login()
def post():
    form = SQLFORM(db.shop)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('done'))
    elif form.errors:
        response.flash = 'input errors'
    else:
        response.flash = "please fill"    
    return locals()

def update():
    record = db.shop(request.args(0) or redirect(URL('post')))
    form = SQLFORM(db.shop, record)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('done'))
    elif form.errors:
        response.flash = 'input errors'
    else:
        response.flash = "please fill"    
    return locals()

def done():
    return locals()

def data():
    rows = db(db.shop).select()
    return locals()

def view():
    rows = db(db.shop).select(orderby=~db.shop.id)
    return locals()

def have_user():
    user_dict = {}
    user_rows = db(db.auth_user).select()
    for x in user_rows:
        user_dict[x.id] = x.last_name + " " + x.first_name

    sql = """
        SELECT shop.id,shop.shop_item, shop.shop_info, shop.shop_locate, shop.shop_date_post, user_shop.name, user_shop.id 
        FROM shop, user_shop WHERE shop.shop_user_id = user_shop.id;
    """
    rows = db.executesql(sql)
    return locals()