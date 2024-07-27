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