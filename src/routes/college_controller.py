from flask import Blueprint, jsonify, render_template, request
from werkzeug import Response
from src.forms import CollegeForm
from src.entities import College
from src.model import SSIS
from src.routes import iterator_is_empty

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route('', methods=['GET'])
def load_colleges() -> str:
    """
    Load the colleges content with an optional search filter.
    """
    # Get the search query and field from the request arguments
    search_query = request.args.get("search", "", type=str).strip().upper()
    search_field = request.args.get("field", "code", type=str).strip().lower()

    # Fetch colleges based on the search query and selected field if provided
    if search_query and search_field in ["code", "name"]:
        filter_kwargs = {search_field: search_query}  # Create a dynamic filter using the selected field
        colleges, is_empty = iterator_is_empty(SSIS.get_colleges(**filter_kwargs))
    else:
        colleges, is_empty = iterator_is_empty(SSIS.get_colleges())  # Fetch all colleges if no search query

    # Create a form instance for use in the modal
    college_form = CollegeForm()
    return render_template(
        'colleges_content.html', 
        colleges=colleges, 
        college_form=college_form, 
        is_empty=is_empty, 
        search_query=search_query,
        search_field=search_field
    )


@colleges_bp.route('/add', methods=['POST'])
def add_college() -> Response:
    """
    Handle form submission for adding a college.
    """
    form = CollegeForm()
    if form.validate_on_submit():
        new_college = College(
            code=form.code.data.upper(),
            name=form.name.data.upper(),
        )
        
        SSIS.add_college(new_college)
        
        # Return JSON response for AJAX success handling
        return jsonify(success=True, message="College added successfully!")
    
    # Return error message if form validation fails
    return jsonify(success=False, message=f"College {str(form.code.data)!r} already exists!")


@colleges_bp.route('/edit', methods=['POST'])
def edit_college() -> Response:
    """
    Handle form submission for editing an existing college.
    """
    form = CollegeForm()
    
    college = SSIS.get_college(str(form.code.data))
    if college:
        # Update the college with form data
        college.name = form.name.data.upper()
        
        try:
            SSIS.edit_college(college)
            # Return JSON response for AJAX success handling
            return jsonify(success=True, message="College updated successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Error: {e}")
    
    return jsonify(success=False, message=f"Program {str(form.code.data)!r} does not exist!")


@colleges_bp.route('/delete', methods=['POST'])
def delete_college() -> Response:
    """
    Route to handle deletion of a college by code.
    """
    college_code = request.form.get('code')
    
    if college_code:
        try:
            SSIS.delete_college(college_code)
            return jsonify(success=True, message="College deleted successfully!")
        
        except Exception as e:
            return jsonify(success=False, message=f"Failed to delete college\nError: {e}")
    
    return jsonify(success=False, message="Invalid college code.")
