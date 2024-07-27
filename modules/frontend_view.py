from gluon.html import *

class FrontendView:

    def show_button(self, href: str, text: str, class_name: str):
        button = H5(A(text, _href=href, _class=class_name, _style="padding: 10px; border-radius: 10px;"), _style="padding: 10px;")
        return button

    def show_buttons(self, list_button):
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

    def flex_button(self, list_button):
        button = DIV(list_button, _style="display: flex;")
        return button

    def show_table(self, th_list, column_list, table):
        try:
            th = TH(XML("".join(str(TD(B(name))) for name in th_list)))
            tr = [
                TR(
                    *[TD(B(x.get(col))) for col in column_list]
                )
                for x in table
            ]
            table_element = TABLE(th, *tr, _class="table")
            return table_element
        except NameError as e:
            print(f"NameError: {e}")
            return e
        except Exception as e:
            print(f"Unexpected error: {e}")
            return e

    def display_body(self, head, button, content):
        form = BODY(head,button,content)
        return form

    def add_header(self):
        header = HEAD(
            LI(
                _href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
                _rel="stylesheet"
            ), 
            SCRIPT(
                _src="URL('static', 'js/more.js')"
            )
        )
        return header