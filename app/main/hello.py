# -*- coding: utf-8 -*-
"""
Created on 2018/12/14 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask import Flask,  redirect, render_template, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)
manager = Manager(app)


app.config['SECRET_KEY'] = 'HARD TO GUESS STRING'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@127.0.0.1:3306/Flasky'
# 来启用自动提交数据库更改在每个请求中
# 由SQLAlchemy实例化的db对象表示数据库且提供访问Flask-SQLAlchemy的所有功能
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 994
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False ## 默认就是 false, 加上警示自己

# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = 'javaxxl@163.com'
app.config['MAIL_PASSWORD'] = ''
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <javaxxl@163.com>'
app.config['FLASKY_ADMIN'] = 'javaxxl@163.com'

bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
mail = Mail(app)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # users = db.relationship('User', backref='role', lazy='subquery')
    users = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # roles = db.relationship('Role', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['POST', 'GET'])
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
        return redirect(url_for('index'))
    return render_template('index.html',form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    # return '<h1>nice to meet you, %s!</h1>' % name
    return render_template('user3.html', name=name)



@app.route('/ask/', methods=['GET', 'POST'])
def ask():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('ask.html', form=form, name=name)


@app.route('/info/', methods=['GET', 'POST'])
def info():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('info'))
    return render_template('info.html', form=form, name=session.get('name'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def interal_server_error(e):
    return render_template('500.html'), 500

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

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run(debug=True)