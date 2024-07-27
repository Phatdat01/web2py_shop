from form_action import FormAction
from frontend_view import FrontendView

@auth.requires_login()
def post():
    form = SQLFORM(db.shop)
    form_process = FormAction()
    view_process = FrontendView()

    head = H1("Post shop Demo")
    button = view_process.show_button(
        href=URL('demo','shop','view'),
        text="Cancel",
        class_name="btn-danger"
    )
    form = form_process.form_accepted(form=form)    
    form = view_process.display_body(head=head,button=button,content=form)
    return dict(form=form)

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
    view_process = FrontendView()
    head = H1("Action Successfully!!!")
    button = view_process.show_button(
        href=URL('demo','shop','view'),
        text="Return to Home!",
        class_name="btn-primary"
    )
    form = view_process.display_body(head=head,button=button,content="")
    return dict(form=form)

def view():
    view_process = FrontendView()

    button = view_process.show_buttons(
        list_button=[
            [URL('demo','shop','post'),"Add Item"],
            [URL('demo','provider','data'),"Membership"],
            [URL('demo','shop','have_user'),"User"],
            [URL('demo','carts','index'),"Cart"]
        ]
    )

    rows = db(db.shop).select(orderby=~db.shop.id)
    user_dict = {}
    user = db(db.auth_user).select()
    for x in user:
        user_dict[x.id] = x.last_name + " " + x.first_name
    return dict(
        button=button,
        user_dict=user_dict,
        rows=rows
    )

def have_user():
    view_process = FrontendView()
    user_dict = {}
    user_rows = db(db.auth_user).select()
    for x in user_rows:
        user_dict[x.id] = x.last_name + " " + x.first_name
    has_membership = auth.has_membership('create_user')
    
    list_button =[[URL('demo','shop','view'),"Return to Home Web"]]
    if has_membership:
        list_button.insert(0,[URL('demo','user_shop','view'),"Show List User"])
    button = view_process.show_buttons(list_button=list_button)
    
    # Query Not injection
    query = (db.shop.shop_user_id == db.user_shop.id)
    fields = [
        db.shop.id,
        db.shop.shop_item,
        db.shop.shop_info,
        db.shop.shop_locate,
        db.shop.shop_date_post,
        db.user_shop.name,
        db.user_shop.id
    ]
    rows = [
        tuple(row[field] for field in fields)
        for row in db(query).select(*fields)
    ]

    return dict(
        button=button,
        rows=rows,
        user_dict=user_dict
    )