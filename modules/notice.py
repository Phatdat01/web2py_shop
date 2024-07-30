from gluon.tools import Mail

class Notice:
    def mail_item_notice(self, mail_to_list, action, item, num):
        mail = Mail()

        mail.settings.server = 'smtp.gmail.com:465'
        mail.settings.ssl = True
        mail.settings.sender = 'nguyen123lht@gmail.com'
        mail.settings.login = 'nguyen123lht@gmail.com:pnts bdma ospp goxk'
        mail.send(
            to=mail_to_list,
            subject='JUST HAVE USER ADD ITEM TO CART',
            message=f"Hi, I'm testing send message from web2py! \nJust have the cart {action} {num} {item} item!!!"
        )