from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from werkzeug import Response
from src.forms import StudentForm
from src.entities import Student, Gender
from src.model import SSIS

students_bp = Blueprint("students", __name__)

@students_bp.route('', methods=['GET'])
def load_students():
    """Load the students content with an optional search filter."""
    # Get the search query from the request arguments
    search_query = request.args.get("search", "", type=str).strip()

    # Fetch students based on the search query if provided, otherwise get all students
    if search_query:
        students = list(SSIS.get_students(id=search_query))  # Search by student ID only
    else:
        students = list(SSIS.get_students())

    # Fetch programs to populate the StudentForm's program dropdown choices
    program_choices = [(program.code, program.name) for program in SSIS.get_programs()]

    # Create a StudentForm instance with dynamic program choices
    student_form = StudentForm(program_list=program_choices)

    return render_template('students_content.html', students=students, student_form=student_form)


@students_bp.route('/add_student', methods=['POST'])
def add_student():
    """
    Route to handle form submission for adding a new student.
    Validates the form and adds the student to the database.
    """
    # Get the program choices again to pass to the form for validation
    program_choices = [(program.code, program.name) for program in SSIS.get_programs()]
    form = StudentForm(program_list=program_choices, formdata=request.form)

    if form.validate_on_submit():
        # Create a new Student instance with the form data
        new_student = Student(
            id=form.id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            year=form.year.data,
            gender=form.gender.data,
            program=form.program.data
        )
        try:
            # Add the student to the database
            SSIS.add_student(new_student)
            flash("Student added successfully!", "success")
            return redirect(url_for('students.load_students'))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    # If validation or addition fails, re-render the students template with errors
    return redirect(url_for('students.load_students'))


@students_bp.route('/edit_student/<string:student_id>', methods=['POST'])
def edit_student(student_id):
    """
    Route to handle form submission for editing an existing student.
    Validates the form and updates the student in the database.
    """
    # Get the program choices again to pass to the form for validation
    program_choices = [(program.code, program.name) for program in SSIS.get_programs()]
    form = StudentForm(program_list=program_choices, formdata=request.form)

    if form.validate_on_submit():
        # Fetch the existing student from the database
        student = SSIS.get_student(student_id)
        if student:
            # Update the student with the new form data
            student.firstname = form.firstname.data
            student.lastname = form.lastname.data
            student.year = form.year.data
            student.gender = form.gender.data
            student.program = form.program.data
            try:
                # Update the student in the database
                SSIS.edit_student(student)
                flash("Student updated successfully!", "success")
                return redirect(url_for('students.load_students'))
            except Exception as e:
                flash(f"Error: {e}", "danger")

    # If validation or update fails, re-render the students template with errors
    return redirect(url_for('students.load_students'))


@students_bp.route('/delete_student', methods=['POST'])
def delete_student() -> Response:
    """
    Route to handle deletion of a student by ID.
    Returns a JSON response indicating success or failure.
    """
    student_id = request.form.get('id')
    
    if student_id is not None:
        try:
            SSIS.delete_student(student_id)
            flash("Student deleted successfully", "success")
        
        except Exception as e:
            flash(f"Failed to delete student\nError: {e}", "danger")
    
    return redirect(url_for('students.load_colleges'))
