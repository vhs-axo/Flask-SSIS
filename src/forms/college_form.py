from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

class CollegeForm(FlaskForm):
    code = StringField(
        "College Code", 
        validators=[
            validators.DataRequired(message="College Code is required.")
        ]
    )
    name = StringField(
        "College Name", 
        validators=[
            validators.DataRequired(message="College Name is required.")
        ]
    )
    save = SubmitField("Save")
