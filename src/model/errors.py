class CollegeExistsError(Exception):
    """Exception raised when attempting to add a college with a duplicate code."""
    def __init__(self, college_code: str) -> None:
        super().__init__(f"College with code {college_code!r} already exists.")

class CollegeNotFoundError(Exception):
    """Exception raised when a college with a specified code is not found."""
    def __init__(self, college_code: str) -> None:
        super().__init__(f"College with code {college_code!r} not found.")

class ProgramExistsError(Exception):
    """Exception raised when attempting to add a program with a duplicate code."""
    def __init__(self, program_code: str) -> None:
        super().__init__(f"Program with code {program_code!r} already exists.")

class ProgramNotFoundError(Exception):
    """Exception raised when a program with a specified code is not found."""
    def __init__(self, program_code: str) -> None:
        super().__init__(f"Program with code {program_code!r} not found.")

class StudentExistsError(Exception):
    """Exception raised when attempting to add a student with a duplicate ID."""
    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student with ID {student_id!r} already exists.")
        
class StudentNotFoundError(Exception):
    """Exception raised when a student with a specified ID is not found."""
    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student with ID {student_id!r} not found.")
