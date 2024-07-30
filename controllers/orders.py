from frontend_view import FrontendView

class Orders:
    def index(self):
        shop_dict = []
        user_dict = []
        auth_creater = auth.has_membership('create_user')
        try:
            if auth_creater:
                rows = db(db.orders).select()
            else:
                rows = db(db.orders.user_id == auth.user.id).select()
            shops = db(db.shop).select()
            shop_dict = {row.id: (row.shop_item, row.shop_img, row.num) for row in shops}
            user_rows = db(db.auth_user).select()
            user_dict = {x.id: f"{x.last_name} {x.first_name}" for x in user_rows}
        except Exception as e:
            rows = []
        return rows, shop_dict, auth_creater, user_dict, table

@auth.requires_login()
def index(): 
    view_process = FrontendView()
    rows = db((db.orders.cart_id==db.carts.id) & (db.carts.shop_id==db.shop.id)).select(
            db.orders.id,
            db.carts.id,
            db.shop.shop_item,
            db.shop.shop_img,
            db.carts.user_id,
            db.carts.num,
            db.shop.num
    )
    head = H1("All Purchased")
    button = view_process.show_button(
        href=URL('web2py_shop','shop','view'),
        text="Continue purchase!",
        class_name="btn-success"
    )
    th_list=["","Shop Item","Num"]
    column_list=["orders.id", "shop.shop_img","shop.shop_item","carts.num", "carts.user_id"]
    table = view_process.show_table(
        th_list=th_list,
        column_list=column_list,
        table=rows,
        permission=auth.has_membership('create_user')
    )
    form = view_process.display_body(head=head,button=button,content=table)
    return dict(form=form)

@auth.requires_login()
def done():
    view_process = FrontendView()
    button = view_process.show_buttons(
        list_button=[
            [URL('web2py_shop','orders','index'),'See your purchased!'],
            [URL('web2py_shop','carts','index'),'Return to Cart']
        ]
    )

    head = H1("You just purchase successfully!! \nThank you!")
    form = view_process.display_body(head=head,button=button,content="")
    return dict(form=form)
    
@auth.requires_login()
def purchase():
    if request.method == 'POST':
        try:
            data = request.vars
            cart_id = int(data.id)
            db.orders.insert(cart_id=cart_id)
            redirect(URL('web2py_shop','orders','done'))
            return locals()
        except Exception as e:
            print(e)
            redirect(URL('web2py_shop','carts','index'))