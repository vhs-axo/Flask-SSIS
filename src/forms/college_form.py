from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import Field, StringField, ValidationError, validators, SubmitField

from src.model import SSIS

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

    def validate_code(self, field: Field) -> None:
        """Check if the student ID already exists in the database."""
        if SSIS.get_college(field.data) is not None:
            raise ValidationError("A college with this code already exists.")
