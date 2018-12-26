# -*- coding: utf-8 -*-
"""
Created on 2018/12/25 - the current system date.

__auther__ = 'xiaoliang'
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('submit')

