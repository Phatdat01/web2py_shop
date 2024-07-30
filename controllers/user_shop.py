from form_action import FormAction
from frontend_view import FrontendView

def index():
    return dict(message="Hello from user shop")

@auth.requires_membership('create_user')
def data():
    rows = db(db.user_shop).select()
    return locals()

def count_user():
    num = db(db.user_shop).count()
    return locals()

def done():
    return locals()

@auth.requires_membership('create_user')
def post():
    form_process = FormAction()
    form = SQLFORM(db.user_shop)
    view_process = FrontendView()

    head = H1("Create New User")
    button = view_process.show_button(
        href=URL("web2py_shop","user_shop","view"),
        text="Cancel",
        class_name="btn-danger"
    )

    form = form_process.form_accepted(form=form)
    form = view_process.display_body(head=head,button=button,content=form)
    return dict(form=form)

def update():
    form_process = FormAction()
    record = db.user_shop(request.args(0) or redirect(URL('post')))
    form = SQLFORM(db.user_shop, record)
    form = form_process.form_accepted(form=form)
    return form

@auth.requires_membership('create_user')
def view():
    rows = db(db.user_shop).select(orderby=db.user_shop.id)
    th_list = ["Name","Phone"]
    column_list = ['id', 'name', 'phone']

    view_process = FrontendView()

    head = H1("This is Page show User")
    button = view_process.show_buttons(
        list_button=[
            [URL('web2py_shop','user_shop','post'),"Add"],
            [URL('web2py_shop','shop','have_user'),"Return to Shop User"]
        ]
    )
    content = view_process.show_table(th_list,column_list,rows)
    
    form = view_process.display_body(head=head, button=button, content=content)
    return dict(form=form)