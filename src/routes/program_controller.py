from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from werkzeug import Response
from src.forms import ProgramForm
from src.entities import Program
from src.model import SSIS

programs_bp = Blueprint("programs", __name__)

@programs_bp.route('', methods=['GET'])
def load_programs():
    """Load the programs content with an optional search filter."""
    # Get the search query from the request arguments
    search_query = request.args.get("search", "", type=str).strip()

    # Fetch students based on the search query if provided, otherwise get all students
    if search_query:
        programs = list(SSIS.get_programs(code=search_query))  # Search by student ID only
    else:
        programs = list(SSIS.get_programs())

    # Fetch colleges to populate the ProgramForm's college dropdown choices
    college_choices = [(college.code, college.name) for college in SSIS.get_colleges()]

    # Create a ProgramForm instance with dynamic college choices
    program_form = ProgramForm(college_list=college_choices)

    return render_template('programs_content.html', programs=programs, program_form=program_form)


@programs_bp.route('/add_program', methods=['POST'])
def add_program():
    """Handle form submission for adding a program."""
    form = ProgramForm()
    if form.validate_on_submit():
        new_program = Program(
            code=form.code.data,
            name=form.name.data,
            college=form.college.data,
        )
        try:
            SSIS.add_program(new_program)
            flash("Program added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return redirect(url_for('programs.load_programs'))


@programs_bp.route('/edit_program/<string:program_code>', methods=['POST'])
def edit_program(program_code) -> Response:
    """Handle form submission for editing an existing program."""
    program_choices = [(college.code, college.name) for college in SSIS.get_colleges()]
    form = ProgramForm(program_list=program_choices, formdata=request.form)

    if form.validate_on_submit():
        program = SSIS.get_program(program_code)
        if program:
            # Update the program with form data
            program.name = form.name.data
            program.college = form.college.data
            try:
                SSIS.edit_program(program)
                flash("Program updated successfully!", "success")
            except Exception as e:
                flash(f"Error: {e}", "danger")
    return redirect(url_for('programs.load_programs'))


@programs_bp.route('/delete_program', methods=['POST'])
def delete_program() -> Response:
    """
    Route to handle deletion of a student by ID.
    Returns a JSON response indicating success or failure.
    """
    program_code = request.form.get('code')
    
    if program_code is not None:
        try:
            SSIS.delete_program(program_code)
            flash("Program deleted successfully", "success")
        
        except Exception as e:
            flash(f"Failed to delete program\nError: {e}", "danger")
    
    return redirect(url_for('programs.load_colleges'))
