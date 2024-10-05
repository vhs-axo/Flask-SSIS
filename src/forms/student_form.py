from __future__ import annotations
from typing import Iterable

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, validators, SubmitField, SelectField, RadioField, Field

from src.entities import Student, Gender
from src.model import SSIS

class StudentForm(FlaskForm):
    id = StringField(
        "Student I.D.", 
        validators=[
            validators.DataRequired(),
            validators.Regexp(Student.ID_VALID_REGEX, message="Invalid ID format. Must follow the pattern YYYY-NNNN.")
        ],
        render_kw={"placeholder": "YYYY-NNNN"}
    )
    firstname = StringField(
        "First Name(s)", 
        validators=[
            validators.DataRequired(message="First name is required.")
        ],
        render_kw={"placeholder": "e.g. JUAN PONCE, ..."}
    )
    lastname = StringField(
        "Last Name", 
        validators=[
            validators.DataRequired(message="Last name is required.")
        ],
        render_kw={"placeholder": "e.g. ENRILE, ..."}
    )
    year = SelectField(
        "Year Level", 
        validators=[
            validators.DataRequired(message="Year level is required.")
        ], 
        choices=tuple((str(year), str(year)) for year in range(1, Student.YEAR_MAX_LEVEL + 1)),
        coerce=int
    )
    gender = RadioField(
        "Gender", 
        validators=[
            validators.DataRequired(message="Gender is required.")
        ], 
        choices=tuple((gender.value, str(gender)) for gender in Gender),
        coerce=Gender
    )
    program = SelectField(
        "Program", 
        validators=[
            validators.DataRequired(message="Program is required.")
        ]
        # Choices will be dynamically populated with a list of programs in the form
    )
    save = SubmitField("Save")

    def __init__(self, program_list: Iterable[tuple[str, str]], *args, **kwargs) -> None:
        """Initialize the form and populate dynamic fields."""
        super().__init__(*args, **kwargs)

        self.program.choices = program_list # type: ignore
    
    def validate_id(self, field: Field) -> None:
        """Check if the student ID already exists in the database."""
        if SSIS.get_student(field.data) is not None:
            raise ValidationError("A student with this ID already exists.")
