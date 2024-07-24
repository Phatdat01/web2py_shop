# -*- coding: utf-8 -*-
# try something like

def first_step():
    mess = "Hello my name is Dat"
    return locals()

def alo():
    all = "Super man Dat"
    return locals()

def multiply():
    arg1 = 0
    arg2 = 0
    # if request.args:
    #     arg1 = float(request.args(0))
    #     arg2 = float(request.args(1))
    if request.post_vars:
        arg1 = float(request.post_vars.arg1)
        arg2 = float(request.post_vars.arg2)
    multiply = arg1*arg2
    return locals()

def request_objects():
    app=request.application
    cntr=request.controller
    fx=request.function
    extn=request.extension
    folder=request.folder
    now=request.now
    client=request.client
    isSecure=request.is_https
    return locals()

def index(): return dict(message="hello from basics.py")
