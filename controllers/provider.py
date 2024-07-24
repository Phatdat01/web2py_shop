# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from provider.py")

def form():
    form = SQLFORM.factory(
        Field('name', requires = IS_NOT_EMPTY()),
        Field('membership', requires = IS_IN_SET(['individual','company','family']))
    )
    if form.process().accepted:
        response.flash = 'form accepted'
        session.name = form.vars.name
        session.membership = form.vars.membership
        redirect(URL('form_accepted'))
    elif form.errors:
        response.flash = 'form errors'
    return locals()

def form_accepted():
    title = "Good work"
    return locals()