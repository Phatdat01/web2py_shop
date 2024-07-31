from gluon.html import *
from typing import List

class FrontendView:

    def show_button(self, href: str, text: str, class_name: str):
        button = H5(A(text, _href=href, _class=class_name, _style="padding: 10px; border-radius: 10px;"), _style="padding: 10px;")
        return button

    def show_buttons(self, list_button):
        """
        Display a list[[url, btn_name],...] to a row (display flex)
        """
        list_class_name = ["btn-success","btn-primary","btn-secondary","btn-danger"]
        lst_btn = []
        for i in range(len(list_button)):
            btn = self.show_button(
                href=list_button[i][0],
                text=list_button[i][1],
                class_name=list_class_name[i]
            )
            lst_btn.append(btn)
        button = self.flex_button(lst_btn)
        return button
    
    def show_change_btn(self, id, num):
        """
        Show button relate to up or down
        """
        text = "+" if num > 0 else "-"
        btn = BUTTON(
            text,
            _type="button",
            _onclick=f"changeQuantityWithAjax('{id}', {num})"
        )
        return btn
    
    def show_action_btn(self, url: str, id: str, text, class_name: str = "", style: str = ""):
        """
        display btn with submit
        """
        td = FORM(
            INPUT(
                _type="hidden",
                _name="id",
                _value=id
            ),
            BUTTON(
                text,
                _type="submit",
                _class=class_name,
                _style= style
            ),

            _action = url,
            _method = "post"
        )
        return td

    def flex_button(self, list_button):
        button = DIV(list_button, _style="display: flex;")
        return button

    def check_col(self, x, is_cart, col, permission: bool = False):
        value_col = x.get(col)
        # Check purchase button
        if col == "add_btn":
            td =TD(
                INPUT(_name = "check", _value ="0", _hidden=True, _id=f"check_{x.get('carts.id')}"),
                BUTTON("Add",
                    _class="btn-secondary",
                    _id = f"btn_{x.get('carts.id')}",
                    _onclick=f"changeRowColorAndCheck({x.get('carts.id')})"
                )
            )   

            # self.show_action_btn(
            #     url=URL('web2py_shop', 'orders','purchase'),
            #     class_name="btn-secondary",
            #     text="Add",
            #     id=x.get("carts.id")
            # )
        # Check delete button
        elif col == "delete_btn":
            td = self.show_action_btn(
                url=URL('web2py_shop', 'carts','delete'),
                style="background: none;",
                text= I(_class="fas fa-trash"),
                id=x.get("carts.id")
            )
        elif col == "show_user":
            hidden = True
            if permission == True:
                hidden = False
            td = TD(f"{x.get('auth_user.last_name')} {x.get('auth_user.first_name')}", _hidden=hidden)
        #Check web is cart, if right, add change number
        elif is_cart and col =="carts.num":
            td = FORM(
                self.show_change_btn(x.get('carts.id'), -1),
                INPUT(  
                    _type="number",
                    _name="quantity",
                    _min=1,
                    _max=x.get("shop.num"),
                    _value=value_col,
                    _style="width: 50px; border: none;",
                    _id=f"quantity{x.get('carts.id')}",
                    _readonly= True
                ),
                self.show_change_btn(x.get('carts.id'), 1),

                _class="quantity-form",
                _method="post"
            )
        # Check col is image
        elif isinstance(value_col, str) and (value_col.startswith("http://") or value_col.startswith("https://")):
            td = IMG(_src=value_col, _height="50px", _width="50px")
        else:
            td = value_col
        return td

    def check_th(self, name):
        if name =="All":
            td = B(
                    INPUT(_name = "check", _value ="0", _hidden=True, _id=f"check_all"),
                    BUTTON("All",
                        _class="btn-success",
                        _id = f"btn_all",
                        _onclick=f"changeAllRow()"
                    )
                )
        else:
            td = B(name)
        return td

    def show_table(self, th_list: List[str], column_list: List[str], table, is_cart: bool = False, permission:bool=False):
        try:
            if table:
                th = TH()
                for name in th_list:
                    th.append(TD(self.check_th(name)))
                tr = [
                    TR(
                        *[TD(self.check_col(x,is_cart,col, permission)) for col in column_list]
                    )
                    for x in table
                ]
                table_element = TABLE(th, *tr, _class="table")
                return table_element
            return H1("No Item Found!")
        except NameError as e:
            print(f"NameError: {e}")
            return e
        except Exception as e:
            print(f"Unexpected error: {e}")
            return e

    def display_body(self, head, button, content):
        form = BODY(head,button,content)
        return form