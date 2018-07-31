from threading import Thread

from flask_mail import Message
from flask import current_app, render_template

from app.__init__ import mail


def send_async_email(app, msg):
    print('-------1-------')
    with app.app_context():
        try:
            print('-------2-------')
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[Flasky]'+' '+subject,
                  sender=app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template+'.html', **kwargs)
    print('-------6-------')
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
