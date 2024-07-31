from frontend_view import FrontendView

class Orders:
    def index(self):
        view_process = FrontendView()
        auth_creater = auth.has_membership('create_user')
        if auth_creater:
            rows = db((db.auth_user.id==db.carts.user_id) & (db.orders.cart_id==db.carts.id) & (db.carts.shop_id==db.shop.id)).select(orderby=~db.orders.id)
        else:
            rows = db((db.auth_user.id==db.carts.user_id) & (db.carts.user_id == auth.user.id) & (db.orders.cart_id==db.carts.id) & (db.carts.shop_id==db.shop.id)).select(orderby=~db.orders.id)

        head = H1("All Purchased")
        button = view_process.show_buttons(
            list_button=[
                [URL('web2py_shop','carts','index'),"Return to Cart!"],
                [URL('web2py_shop','shop','view'),"Continue purchasing!"]
            ]
        )
        th_list=["","Shop Item","Num"]
        column_list=["orders.id", "shop.shop_img","shop.shop_item","carts.num", "show_user"]
        table = view_process.show_table(
            th_list=th_list,
            column_list=column_list,
            table=rows,
            permission=auth.has_membership('create_user')
        )
        form = view_process.display_body(head=head,button=button,content=table)
        return form

@auth.requires_login()
def index(): 
    orders_show = Orders()
    form = orders_show.index()
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
        done = False
        try:
            data = request.vars
            cart_id = int(data.id)
            db.orders.insert(cart_id=cart_id)
            done = True
            redirect(URL('orders','done'))
        except Exception as e:
            print(e)
            if done:
                redirect(URL('orders','done'))
            redirect(URL('web2py_shop','carts','index'))