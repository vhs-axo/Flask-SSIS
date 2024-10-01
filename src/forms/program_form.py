from __future__ import annotations
from typing import Iterable

from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField

from src.entities import Student, Gender
from src.model import SSIS

class ProgramForm(FlaskForm):
    code = StringField(
        "Program Code", 
        validators=[
            validators.DataRequired(message="Program Code is required.")
        ]
    )
    name = StringField(
        "Program Name", 
        validators=[
            validators.DataRequired(message="Program Name is required.")
        ]
    )
    college = SelectField(
        "College", 
        validators=[
            validators.DataRequired(message="College is required.")
        ]
    )
    save = SubmitField("Save")

    def __init__(self, college_list: Iterable[tuple[str, str]], *args, **kwargs) -> None:
        """Initialize the form and populate dynamic fields."""
        super().__init__(*args, **kwargs)

        self.college.choices = college_list # type: ignore
