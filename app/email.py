# -*- coding: utf-8 -*-
"""
Created on 2018/12/25 - the current system date.

__auther__ = 'xiaoliang'
"""
from flask_mail import Message
from flask import render_template



def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    # mail.send(msg)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)