# -*- coding: utf-8 -*-
"""
Created on 2018/12/14 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask import Flask


app = Flask("try1")


@app.route('/')
def index():
    return '<html><body><head>hello world</head></body></html>'




if __name__=="__main__":
    app.run(debug=True)