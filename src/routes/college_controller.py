from flask import Blueprint, jsonify, render_template, request
from werkzeug import Response
from src.forms import CollegeForm
from src.entities import College
from src.model import SSIS

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route('', methods=['GET'])
def load_colleges() -> str:
    """
    Load the colleges content with an optional search filter.
    """
    # Get the search query from the request arguments
    search_query = request.args.get("search", "", type=str).strip().upper()

    # Fetch colleges based on the search query if provided
    if search_query:
        colleges = SSIS.get_colleges(code=search_query, name=search_query)
    else:
        colleges = SSIS.get_colleges()  # Fetch all colleges if no search query

    # Create a form instance for use in the modal
    college_form = CollegeForm()
    return render_template('colleges_content.html', colleges=colleges, college_form=college_form)


@colleges_bp.route('/add', methods=['POST'])
def add_college() -> Response:
    """
    Handle form submission for adding a college.
    """
    form = CollegeForm()
    if form.validate_on_submit():
        new_college = College(
            code=form.code.data,
            name=form.name.data,
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
        college.name = form.name.data
        
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
