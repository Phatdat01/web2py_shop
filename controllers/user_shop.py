from frontend_view import FrontendView

def index():
    return dict(message="Hello from user shop")

@auth.requires_membership('create_user')
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

@auth.requires_membership('create_user')
def view():
    rows = db(db.user_shop).select(orderby=db.user_shop.id)
    th_list = ["Name","Phone"]
    column_list = ['id', 'name', 'phone']

    process = FrontendView()
    add_button = process.button(
        href=URL('demo','user_shop','post'),
        text="Add",
        class_name="btn-success"
    )
    return_button = process.button(
        href=URL('demo','shop','have_user'),
        text="Return to Shop User",
        class_name="btn-primary"
    )

    head = H1("This is Page show User")
    button = process.flex_button(list_button=[add_button,return_button])
    content = process.table(th_list,column_list,rows)
    
    form = process.table_explore(head=head, button=button, content=content)
    return dict(form=form)