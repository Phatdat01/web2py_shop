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