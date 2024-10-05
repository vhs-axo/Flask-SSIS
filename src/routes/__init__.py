from typing import Iterator
from itertools import tee

def iterator_is_empty(iter: Iterator) -> tuple[Iterator, bool]:
    iter_orig, iter_test = tee(iter, 2)

    try:
        next(iter_test)  # Attempt to get the first element
        return iter_orig, False
    except StopIteration:
        return iter_orig, True

from src.routes.college_controller import colleges_bp
from src.routes.program_controller import programs_bp
from src.routes.student_controller import students_bp

__all__ = ["colleges_bp", "programs_bp", "students_bp"]