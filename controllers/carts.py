from form_action import FormAction

@auth.requires_login()
def index():
    shop_dict = []
    user_dict = []
    auth_creater = auth.has_membership('create_user')
    try:
        if auth_creater:
            rows = db(db.carts).select()
        else:
            rows = db(db.carts.user_id == auth.user.id).select()
        shops = db(db.shop).select()
        shop_dict = {row.id: (row.shop_item, row.shop_img, row.num) for row in shops}
        user_rows = db(db.auth_user).select()
        user_dict = {x.id: f"{x.last_name} {x.first_name}" for x in user_rows}
    except Exception as e:
        rows = []
    return dict(rows=rows, shop_dict=shop_dict, auth_creater=auth_creater, user_dict=user_dict)

@auth.requires_login()
def post():
    if request.method == 'POST':
        try:
            data = request.vars
            quantity = int(data.quantity)
            shop_id = int(data.shop_id)
            user_id = int(auth.user.id)
            check_row = db((db.carts.shop_id == shop_id) & (db.carts.user_id == user_id)).select().first()
            if check_row:
                id = int(check_row.id)
                redirect((URL('demo','provider','form', vars=dict(id=id,num_change=quantity))))
            current_num = db.shop(shop_id).num  
            new_num = current_num - quantity
            db.carts.insert(shop_id=shop_id, user_id=user_id, num=quantity)
            db(db.shop.id == shop_id).update(num=new_num)
            redirect(URL('demo','carts','index'))
        except Exception as e:
            print(e)
            if check_row:
                redirect(URL('demo','carts','update', vars=dict(id=id,num_change=quantity)))
            redirect(URL('demo','carts','index'))
    else:
        redirect(URL('demo','carts','index'))

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
                redirect(URL('demo','carts','index'))
        except Exception as e:
            print(e)
            redirect(URL('demo','carts','index'))
    else:
        redirect(URL('demo','carts','index'))

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
        if new_num_cart>0 or new_num_shop >=0:
            db(db.shop.id == shop_id).update(num = new_num_shop)
            db(db.carts.id == id).update(num = new_num_cart)
    except Exception as e:
        print(e)
        redirect(URL('demo','carts','index'))
    return redirect(URL('demo','carts','index'))