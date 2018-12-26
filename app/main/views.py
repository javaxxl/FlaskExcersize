# -*- coding: utf-8 -*-
"""
Created on 2018/12/25 - the current system date.

__auther__ = 'xiaoliang'
"""
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from ..models import User
from .. import db
from ..email import send_email
from app import create_app

@main.route('/', methods=['POST', 'GET'])
def index():
    # return render_template('user3.html',name='Rock')


    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)

        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',form=form, name=session.get('name'),known=session.get('known', False),current_time=datetime.utcnow())