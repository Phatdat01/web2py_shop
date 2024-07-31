from gluon import redirect, URL
from gluon.globals import current

class FormAction:

    def form_accepted(self, form):
        if form.process().accepted:
            current.session.flash = "form accepted"
            redirect(URL('done'))
        elif form.errors:
            current.response.flash = "input errors"
        else:
            current.response.flash = "please fill"
        return form

    def check_purchased_row(self, table, list_id):
        try:
            rows = [r for r in table if r.carts.id not in list_id]
        except:
            rows = [r for r in table if r.id not in list_id]
        return rows

    def get_new_shop_item_num(self, db, shop_id, num_change):
        current_num_shop = db.shop(shop_id).num
        new_num_shop = current_num_shop-num_change
        db(db.shop.id == shop_id).update(num = new_num_shop)

    def change_num_item_cart_vs_shop(self, db, id:int = None, shop_id:int = None, user_id:int = None, num:int = None):
        """
        - When insert, just send 3 key: shop_id, user_id,num
        - When delete, just send id
        - When update, just send id, num(num on this is num need change)
        """
        if id:
            if num:
                # update, num on this is num change, and auth to check role
                shop_id = db.carts(id).shop_id
                num_change = num
                current_num_carts = db.carts(id).num
                new_num_cart = current_num_carts+num_change
                if (new_num_cart>0 or (db.shop(shop_id).num-num_change >=0)):
                    db(db.carts.id == id).update(num = new_num_cart)
                else:
                    return "No enough Item on shop!"
            else:    
                # Delete
                shop_id = db.carts(id).shop_id  
                num_change = -db.carts(id).num
                db(db.carts.id == id).delete()
        else:
            # insert
            num_change = num
            row = db.carts.insert(shop_id=shop_id, user_id=user_id, num=num)
        
        self.get_new_shop_item_num(
            db=db,
            shop_id=shop_id,
            num_change=num_change
        )
        if row:
            return row
        return None