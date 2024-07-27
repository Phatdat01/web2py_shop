from gluon.html import *

class FrontendView:

    def show_button(self, href: str, text: str, class_name: str):
        button = H5(A(text, _href=href, _class=class_name, _style="padding: 10px; border-radius: 10px;"), _style="padding: 10px;")
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