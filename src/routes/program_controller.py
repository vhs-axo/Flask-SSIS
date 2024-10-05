from flask import Blueprint, jsonify, render_template, request
from werkzeug import Response
from src.forms import ProgramForm
from src.entities import Program
from src.model import SSIS
from src.routes import iterator_is_empty

programs_bp = Blueprint("programs", __name__)

@programs_bp.route('', methods=['GET'])
def load_programs():
    """
    Load the programs content with an optional search filter.
    """
    # Get the search query and field from the request arguments
    search_query = request.args.get("search", "", type=str).strip().upper()
    search_field = request.args.get("field", "code", type=str).strip().lower()

    # Fetch programs based on the search query and selected field if provided
    if search_query and search_field in ["code", "name", "college"]:
        filter_kwargs = {search_field: search_query}  # Create a dynamic filter using the selected field
        programs, is_empty = iterator_is_empty(SSIS.get_programs(**filter_kwargs))
    else:
        programs, is_empty = iterator_is_empty(SSIS.get_programs())

    # Fetch colleges to populate the ProgramForm's college dropdown choices
    college_choices = [(college.code, college.name) for college in SSIS.get_colleges()]

    # Create a ProgramForm instance with dynamic college choices
    program_form = ProgramForm(college_list=college_choices)

    return render_template(
        'programs_content.html', 
        programs=programs, 
        program_form=program_form, 
        is_empty=is_empty,
        search_query=search_query,
        search_field=search_field
    )


@programs_bp.route('/add', methods=['POST'])
def add_program():
    """
    Handle form submission for adding a program.
    """
    form = ProgramForm(college_list=[(college.code, college.name) for college in SSIS.get_colleges()])
    
    if form.validate_on_submit():
        new_program = Program(
            code=form.code.data.upper(),
            name=form.name.data.upper(),
            college=form.college.data,
        )
        
        SSIS.add_program(new_program)

        # Return JSON response for AJAX success handling
        return jsonify(success=True, message="Program added successfully!")
    
    # Return error message if form validation fails
    return jsonify(success=False, message=f"Program {str(form.code.data)!r} already exists!")


@programs_bp.route('/edit', methods=['POST'])
def edit_program() -> Response:
    """
    Handle form submission for editing an existing program.
    """
    college_choices = [(college.code, college.name) for college in SSIS.get_colleges()]
    
    form = ProgramForm(college_list=college_choices, formdata=request.form)
    
    program = SSIS.get_program(str(form.code.data))
    if program:
        # Update the program with form data
        program.name = form.name.data.upper()
        program.college = form.college.data.upper()
        
        try:
            SSIS.edit_program(program)
            # Return JSON response for AJAX success handling
            return jsonify(success=True, message="Program updated successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Error: {e}")
    
    return jsonify(success=False, message=f"Program {str(form.code.data)!r} does not exist!")


@programs_bp.route('/delete', methods=['POST'])
def delete_program() -> Response:
    """
    Route to handle deletion of a program by code.
    """
    program_code = request.form.get('code')
    
    if program_code:
        try:
            SSIS.delete_program(program_code)
            return jsonify(success=True, message="Program deleted successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Failed to delete program\nError: {e}")
    
    return jsonify(success=False, message="Invalid program code.")
