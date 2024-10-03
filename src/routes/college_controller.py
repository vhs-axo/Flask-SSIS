from flask import jsonify, render_template, request, redirect, url_for, flash, Blueprint
from werkzeug import Response
from src.forms import CollegeForm
from src.entities import College
from src.model import SSIS

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route('', methods=['GET'])
def load_colleges() -> str:
    """Load the colleges content with an optional search filter."""
    # Get the search query from the request arguments
    search_query = request.args.get("search", "", type=str).strip()

    # Fetch colleges based on the search query if provided
    if search_query:
        colleges = list(SSIS.get_colleges(code=search_query))
    else:
        colleges = list(SSIS.get_colleges())  # Fetch all colleges if no search query

    # Create a form instance for use in the modal
    college_form = CollegeForm()
    return render_template('colleges_content.html', colleges=colleges, college_form=college_form)


@colleges_bp.route('/add_college', methods=['POST'])
def add_college() -> Response:
    """Handle form submission for adding a college."""
    form = CollegeForm()
    if form.validate_on_submit():
        new_college = College(
            code=form.code.data,
            name=form.name.data,
        )
        try:
            SSIS.add_college(new_college)
            flash("College added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return redirect(url_for('colleges.load_colleges'))


@colleges_bp.route('/edit_college/<string:college_code>', methods=['POST'])
def edit_college(college_code) -> Response:
    """Handle form submission for editing an existing college."""
    form = CollegeForm()
    if form.validate_on_submit():
        college = SSIS.get_college(college_code)
        if college:
            # Update the college with form data
            college.name = form.name.data
            try:
                SSIS.edit_college(college)
                flash("College updated successfully!", "success")
            except Exception as e:
                flash(f"Error: {e}", "danger")
    return redirect(url_for('colleges.load_colleges'))


@colleges_bp.route('/delete_college', methods=['POST'])
def delete_college() -> Response:
    """
    Route to handle deletion of a student by ID.
    Returns a JSON response indicating success or failure.
    """
    college_code = request.form.get('code')
    
    if college_code is not None:
        try:
            SSIS.delete_college(college_code)
            flash("College deleted successfully", "success")
        
        except Exception as e:
            flash(f"Failed to delete college\nError: {e}", "danger")
    
    return redirect(url_for('colleges.load_colleges'))
