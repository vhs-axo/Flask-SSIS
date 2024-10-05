from __future__ import annotations
from typing import Iterable

from flask_wtf import FlaskForm
from wtforms import Field, StringField, ValidationError, validators, SubmitField, SelectField

from src.model import SSIS

class ProgramForm(FlaskForm):
    code = StringField(
        "Program Code", 
        validators=[
            validators.DataRequired(message="Program Code is required.")
        ],
        render_kw={"placeholder": "e.g. BSCS, BAHIS, ..."}
    )
    name = StringField(
        "Program Name", 
        validators=[
            validators.DataRequired(message="Program Name is required.")
        ],
        render_kw={"placeholder": "e.g. BACHELOR OF SCIENCE IN COMPUTER SCIENCE, ..."}
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
    
    def validate_code(self, field: Field) -> None:
        """Check if the student ID already exists in the database."""
        if SSIS.get_program(field.data) is not None:
            raise ValidationError("A program with this code already exists.")
