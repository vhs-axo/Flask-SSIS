from flask import Blueprint, jsonify, render_template, request
from werkzeug import Response
from src.forms import StudentForm
from src.entities import Student
from src.model import SSIS
from src.routes import iterator_is_empty

students_bp = Blueprint("students", __name__)

@students_bp.route('', methods=['GET'])
def load_students():
    """
    Load the students content with an optional search filter.
    """
    # Get the search query from the request arguments
    search_query = request.args.get("search", "", type=str).strip().upper()

    # Fetch students based on the search query if provided, otherwise get all students
    if search_query:
        students, is_empty = iterator_is_empty(SSIS.get_students(
            id=search_query, firstname=search_query, 
            lastname=search_query, year=search_query, 
            gender=search_query, program=search_query
        ))
    else:
        students, is_empty = iterator_is_empty(SSIS.get_students())

    # Fetch programs to populate the StudentForm's program dropdown choices
    program_choices = [(program.code, program.name) for program in SSIS.get_programs()]

    # Create a StudentForm instance with dynamic program choices
    student_form = StudentForm(program_list=program_choices)

    return render_template('students_content.html', students=students, student_form=student_form, is_empty=is_empty)


@students_bp.route('/add', methods=['POST'])
def add_student():
    """
    Handle form submission for adding a student.
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
        
        SSIS.add_student(new_student)
        
        # Return JSON response for AJAX success handling
        return jsonify(success=True, message="Student added successfully!")

    # Return error message if form validation fails
    return jsonify(success=False, message=f"Student {str(form.id.data)} already exists!")


@students_bp.route('/edit', methods=['POST'])
def edit_student():
    """
    Handle form submission for editing an existing student.
    """
    # Get the program choices again to pass to the form for validation
    program_choices = [(program.code, program.name) for program in SSIS.get_programs()]
    
    form = StudentForm(program_list=program_choices, formdata=request.form)

    student = SSIS.get_student(str(form.id.data))
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
            
            # Return JSON response for AJAX success handling
            return jsonify(success=True, message="Student updated successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Error: {e}")

    return jsonify(success=False, message=f"Student {str(form.id.data)} does not exist!")


@students_bp.route('/delete', methods=['POST'])
def delete_student() -> Response:
    """
    Route to handle deletion of a student by id.
    """
    student_id = request.form.get('id')
    
    if student_id:
        try:
            SSIS.delete_student(student_id)
            return jsonify(success=True, message="Student deleted successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Failed to delete student\nError: {e}")
    
    return jsonify(success=False, message="Invalid student id.")
