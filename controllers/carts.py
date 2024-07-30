from notice import Notice
from form_action import FormAction
from frontend_view import FrontendView
class Carts:
    def index(self):
        view_process = FrontendView()
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
        try:
            data = request.vars
            quantity = int(data.quantity)
            shop_id = int(data.shop_id)
            user_id = int(auth.user.id)
            check_row = db((db.carts.shop_id == shop_id) & (db.carts.user_id == user_id)).select().first()
            
            notice_process = Notice()
            notice_process.mail_item_notice(
                mail_to_list=['nguyen321lht@gmail.com'],
                action="add",
                item=db.shop(shop_id).shop_item,
                num=quantity
            )

            if check_row:
                id = int(check_row.id)
                redirect((URL('web2py_shop','provider','form', vars=dict(id=id,num_change=quantity))))
            current_num = db.shop(shop_id).num  
            new_num = current_num - quantity
            db.carts.insert(shop_id=shop_id, user_id=user_id, num=quantity)
            db(db.shop.id == shop_id).update(num=new_num)
            redirect(URL('web2py_shop','carts','index'))
        except Exception as e:
            print(e)
            if check_row:
                redirect(URL('web2py_shop','carts','update', vars=dict(id=id,num_change=quantity)))
            redirect(URL('web2py_shop','carts','index'))
    else:
        redirect(URL('web2py_shop','carts','index'))

@auth.requires_login()
def delete():
    if request.method == 'POST':
        try:
            data = request.vars
            id = int(data.id)
            if auth.has_membership('create_user') or db.carts(id).user_id == auth.user.id:
                shop_id = db.carts(id).shop_id
                current_num_carts = db.carts(id).num
                current_num_shop = db.shop(shop_id).num
                new_num_shop = current_num_shop + current_num_carts
                db(db.shop.id == shop_id).update(num=new_num_shop)
                db(db.carts.id == id).delete()

                notice_process = Notice()
                notice_process.mail_item_notice(
                    mail_to_list=['nguyen321lht@gmail.com'],
                    action="return",
                    item=db.shop(shop_id).shop_item,
                    num=current_num_carts
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
        data = request.vars
        num_change = int(data.num_change)
        id = int(data.id)
        shop_id = db.carts(id).shop_id
        current_num_carts = db.carts(id).num
        current_num_shop = db.shop(shop_id).num
        new_num_cart = current_num_carts+num_change
        new_num_shop = current_num_shop-num_change
        if (new_num_cart>0 or new_num_shop >=0) and (auth.has_membership('create_user') or db.carts(id).user_id == auth.user.id):
            db(db.shop.id == shop_id).update(num = new_num_shop)
            db(db.carts.id == id).update(num = new_num_cart)
    except Exception as e:
        print(e)
        redirect(URL('web2py_shop','carts','index'))
    return redirect(URL('web2py_shop','carts','index'))