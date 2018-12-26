# -*- coding: utf-8 -*-
"""
Created on 2018/12/25 - the current system date.

__auther__ = 'xiaoliang'
"""
from flask  import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

