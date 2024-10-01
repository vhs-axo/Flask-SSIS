class SSIS:
    INSERT_COLLEGE_QUERY = "INSERT INTO colleges (code, name) VALUES (%s, %s)"
    INSERT_PROGRAM_QUERY = "INSERT INTO programs (code, name, college) VALUES (%s, %s, %s)"
    INSERT_STUDENT_QUERY = "INSERT INTO students (id, firstname, lastname, year, gender, program) VALUES (%s, %s, %s, %s, %s, %s)"

    SELECT_COLLEGE_QUERY = "SELECT * FROM colleges WHERE code = %s"
    SELECT_PROGRAM_QUERY = "SELECT * FROM programs WHERE code = %s"
    SELECT_STUDENT_QUERY = "SELECT * FROM students WHERE id = %s"

    SELECT_COLLEGES_QUERY = "SELECT * FROM colleges ORDER BY code"
    SELECT_PROGRAMS_QUERY = "SELECT * FROM programs ORDER BY code"
    SELECT_STUDENTS_QUERY = "SELECT * FROM students ORDER BY id"

    DELETE_COLLEGE_QUERY = "DELETE FROM colleges WHERE code = %s"
    DELETE_PROGRAM_QUERY = "DELETE FROM programs WHERE code = %s"
    DELETE_STUDENT_QUERY = "DELETE FROM students WHERE id = %s"

    UPDATE_COLLEGE_QUERY = "UPDATE colleges SET name = %s WHERE code = %s"
    UPDATE_PROGRAM_QUERY = "UPDATE programs SET name = %s, college = %s WHERE code = %s"
    UPDATE_STUDENT_QUERY = "UPDATE students SET firstname = %s, lastname = %s, year = %s, gender = %s, program = %s WHERE id = %s"
