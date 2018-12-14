# -*- coding: utf-8 -*-
"""
Created on 2018/12/14 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask import Flask


app = Flask("try1")


@app.route('/')
def index():
    return '<html><body><h1>hello world again</h1></body></html>'

@app.route('/user/<name>')
def user(name):
    return '<h1>nice to meet you, %s!</h1>' % name


if __name__=="__main__":
    app.run(debug=True)