# -*- coding: utf-8 -*-
"""
Created on 2018/12/14 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask import Flask, request, make_response, redirect, abort, render_template


app = Flask("try1")


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    # return "<h1>Bad request</h1>", 400
    # return '<h1>your browser agent: %s</h1>' % user_agent
    """
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
    """
    return redirect('https://www.baidu.com')



@app.route('/user/<name>')
def user(name):
    # return '<h1>nice to meet you, %s!</h1>' % name
    return render_template('user.html',name=name)

"""
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
        return '<h1>Hello, %s</h1>' % user.name
"""


if __name__=="__main__":
    app.run(debug=True)