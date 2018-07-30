from threading import Thread

from flask_mail import Message
from flask import current_app, render_template

from . import email


def send_async_email(app, msg):
    with app.app_context():
        try:
            email.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[Flasky]'+' '+subject,
                  sender=app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
