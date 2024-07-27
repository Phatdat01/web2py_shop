from form_action import FormAction
from frontend_view import FrontendView

def index(): return dict(message="hello from provider.py")

def form():
    # form = SQLFORM.factory(
    #     Field('name', requires = IS_NOT_EMPTY()),
    #     Field('membership', requires = IS_IN_SET(['individual','company','family']))
    # )
    view_process = FrontendView()
    form_process = FormAction()

    head = H1("This is the provider/form.html template")

    button = view_process.show_button(
        href=URL('demo','provider','data'),
        text="Cancel",
        class_name="btn-danger"
    )

    form = SQLFORM(db.provider)
    form = form_process.form_accepted(form)

    form = view_process.display_body(head=head,button=button, content=form)
    return dict(form=form)

def data():
    th_list = ["Name","Membership"]
    column_list = ["id","name","membership"]
    view_process = FrontendView()

    head = H1("This is the provider/data.html template")
    button = view_process.show_buttons(
        list_button=[
            [URL('demo','provider','form'),"Add"],
            [URL('demo','shop','view'),"Return to Home Web"]
    ])
    rows = db(db.provider).select()
    content = view_process.show_table(th_list=th_list,column_list=column_list,table=rows)
    
    form = view_process.display_body(head=head,button=button,content=content)
    return dict(form=form)

def done():
    title = "Good work"
    return locals()