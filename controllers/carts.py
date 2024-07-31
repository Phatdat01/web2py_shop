from notice import Notice
from form_action import FormAction
from frontend_view import FrontendView
class Carts:
    def index(self):
        view_process = FrontendView()
        form_process = FormAction()
        button = view_process.show_buttons(
            list_button=[
                [URL('web2py_shop','orders','index'),"Purchased"],
                [URL('web2py_shop','shop','view'),"Home"]
            ]
        )
        auth_creater = auth.has_membership('create_user')
        if auth_creater:
            rows = db((db.auth_user.id==db.carts.user_id) & (db.carts.shop_id == db.shop.id)).select()
        else:
            rows = db((db.auth_user.id==db.carts.user_id) & (db.carts.shop_id == db.shop.id) & (db.carts.user_id == auth.user.id)).select()

        list_id = [x.cart_id for x in db(db.orders).select(db.orders.cart_id)]
        rows = form_process.check_purchased_row(table=rows, list_id=list_id)
        th_list =["Shop Item","Num"]
        column_list=["carts.id","shop.shop_img","shop.shop_item","carts.num", "show_user","purchase_btn","delete_btn"]
        table = view_process.show_table(
            th_list=th_list,
            column_list=column_list,
            table=rows,
            is_cart=True,
            permission= auth_creater
        )

        form = view_process.display_body(
            head="",
            button=button,
            content=table
        )
        return form

@auth.requires_login()
def index():
    cart_show = Carts()
    form = cart_show.index()
    return dict(form=form)

@auth.requires_login()
def post():
    if request.method == 'POST':
        data = request.vars

        try:
            quantity = int(data.quantity)
            shop_id = int(data.shop_id)
            user_id = int(auth.user.id)

            form_process = FormAction()
            # If this is purchase action on shop
            if data.purchase == "1":
                # insert
                id = form_process.change_num_item_cart_vs_shop(
                    db=db,
                    shop_id=shop_id,
                    user_id=user_id,
                    num=quantity
                )
                print(id)
                db.orders.insert(cart_id=id)
                redirect(URL('web2py_shop','orders','done'))
            check_row = db((db.carts.shop_id == shop_id) & (db.carts.user_id == user_id)).select()
            
            list_id = [x.cart_id for x in db(db.orders).select(db.orders.cart_id)]
            check_row = form_process.check_purchased_row(table=check_row,list_id=list_id)
            
            # Notice
            notice_process = Notice()
            notice_process.mail_item_notice(
                mail_to_list=['nguyen321lht@gmail.com'],
                action="add",
                item=db.shop(shop_id).shop_item,
                num=quantity
            )

            if check_row:
                id = int(check_row[0].id)
                redirect((URL('web2py_shop','provider','form', vars=dict(id=id,num_change=quantity))))

            id = form_process.change_num_item_cart_vs_shop(
                    db=db,
                    shop_id=shop_id,
                    user_id=user_id,
                    num=quantity
            )
            redirect(URL('web2py_shop','carts','index'))
        except Exception as e:
            print(e)
            if data.purchase=="1":
                redirect(URL('web2py_shop','orders','done'))
            elif check_row:
                redirect(URL('web2py_shop','carts','update', vars=dict(id=id,num_change=quantity)))
            redirect(URL('web2py_shop','carts','index'))
    else:
        redirect(URL('web2py_shop','carts','index'))

@auth.requires_login()
def delete():
    if request.method == 'POST':
        try:
            data = request.vars
            form_process = FormAction()
            id = int(data.id)
            list_id = [x.cart_id for x in db(db.orders).select(db.orders.cart_id)]
            if (auth.has_membership('create_user') or db.carts(id).user_id == auth.user.id) and id not in list_id:
                
                # Delete
                new_id = form_process.change_num_item_cart_vs_shop(
                    db=db,
                    id=id
                )
                print("This is delete")
                print(new_id)

                notice_process = Notice()
                notice_process.mail_item_notice(
                    mail_to_list=['nguyen321lht@gmail.com'],
                    action="return",
                    item=db.shop(shop_id).shop_item,
                    num="all"
                )
                redirect(URL('web2py_shop','carts','index'))
        except Exception as e:
            print(e)
            redirect(URL('web2py_shop','carts','index'))
    else:
        redirect(URL('web2py_shop','carts','index'))

@auth.requires_login()
def update():
    try:
        form_process = FormAction()
        list_id = [x.cart_id for x in db(db.orders).select(db.orders.cart_id)]
        data = request.vars
        num_change = int(data.num_change)
        id = int(data.id)
        if auth.has_membership('create_user') or db.carts(id).user_id == auth.user.id  and id not in list_id:
            new_id = form_process.change_num_item_cart_vs_shop(
                db=db,
                id=id,
                num=num_change
            )
            print(new_id)
        else:
            print("No Permission!")
    except Exception as e:
        print(e)
        redirect(URL('web2py_shop','carts','index'))
    return redirect(URL('web2py_shop','carts','index'))