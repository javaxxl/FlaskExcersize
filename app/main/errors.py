# -*- coding: utf-8 -*-
"""
Created on 2018/12/25 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def interal_server_error(e):
    return render_template('500.html'), 500
