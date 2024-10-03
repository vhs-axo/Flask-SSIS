from __future__ import annotations

from collections.abc import Iterator
from typing import Optional, TypeVar

from mysql.connector.cursor import MySQLCursorDict
from mysql.connector import Error, errorcode

from src.entities import College, Program, Student
from src.model.errors import *
from src import mysql

T = TypeVar("T", bound=College | Program | Student)

class SSIS:
    INSERT_COLLEGE_QUERY = "INSERT INTO colleges (code, name) VALUES (%s, %s)"
    INSERT_PROGRAM_QUERY = "INSERT INTO programs (code, name, college) VALUES (%s, %s, %s)"
    INSERT_STUDENT_QUERY = "INSERT INTO students (id, firstname, lastname, year, gender, program) VALUES (%s, %s, %s, %s, %s, %s)"

    SELECT_COLLEGE_QUERY = "SELECT * FROM colleges WHERE code = %s"
    SELECT_PROGRAM_QUERY = "SELECT * FROM programs WHERE code = %s"
    SELECT_STUDENT_QUERY = "SELECT * FROM students WHERE id = %s"

    SELECT_COLLEGES_QUERY = "SELECT * FROM colleges"
    SELECT_PROGRAMS_QUERY = "SELECT * FROM programs"
    SELECT_STUDENTS_QUERY = "SELECT * FROM students"

    DELETE_COLLEGE_QUERY = "DELETE FROM colleges WHERE code = %s"
    DELETE_PROGRAM_QUERY = "DELETE FROM programs WHERE code = %s"
    DELETE_STUDENT_QUERY = "DELETE FROM students WHERE id = %s"

    UPDATE_COLLEGE_QUERY = "UPDATE colleges SET name = %s WHERE code = %s"
    UPDATE_PROGRAM_QUERY = "UPDATE programs SET name = %s, college = %s WHERE code = %s"
    UPDATE_STUDENT_QUERY = "UPDATE students SET firstname = %s, lastname = %s, year = %s, gender = %s, program = %s WHERE id = %s"

    @staticmethod
    def add_college(college: College) -> None:
        try:
            SSIS.__add_entity(SSIS.INSERT_COLLEGE_QUERY, (
                college.code, 
                college.name
            ))
        
        except Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise CollegeExistsError(college.code)
            raise

    @staticmethod
    def add_program(program: Program) -> None:
        try:
            SSIS.__add_entity(SSIS.INSERT_PROGRAM_QUERY, (
                program.code, 
                program.name, 
                program.college
            ))
        
        except Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise ProgramExistsError(program.code)
            raise

    @staticmethod
    def add_student(student: Student) -> None:
        try:
            SSIS.__add_entity(SSIS.INSERT_STUDENT_QUERY, (
                student.id, 
                student.firstname, 
                student.lastname, 
                student.year, 
                student.gender.value, 
                student.program
            ))
        
        except Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise StudentExistsError(student.id)
            raise

    @staticmethod
    def get_college(college_code: str) -> Optional[College]:
        try:
            return SSIS.__get_entity(SSIS.SELECT_COLLEGE_QUERY, college_code, College)
        
        except Error as e:
            print(f"Error: {e}")
            raise
    
    @staticmethod
    def get_program(program_code: str) -> Optional[Program]:
        try:
            return SSIS.__get_entity(SSIS.SELECT_PROGRAM_QUERY, program_code, Program)
        
        except Error as e:
            print(f"Error: {e}")
            raise
    
    @staticmethod
    def get_student(student_id: str) -> Optional[Student]:
        try:
            return SSIS.__get_entity(SSIS.SELECT_STUDENT_QUERY, student_id, Student)
        
        except Error as e:
            print(f"Error: {e}")
            raise
    
    @staticmethod
    def get_colleges(**filter) -> Iterator[College]:
        try:
            query = SSIS.SELECT_COLLEGES_QUERY

            # Build dynamic WHERE clause based on provided filters
            if filter:
                params = []
                conditions = []

                for column, value in filter.items():
                    conditions.append(f"{column} LIKE %s")
                    params.append(f"%{value}%")

                query += " WHERE " + " OR ".join(conditions)
                
                return SSIS.__get_entites(f"{query} ORDER BY id", College, tuple(params))

            return SSIS.__get_entites(f"{query} ORDER BY id", College)
        
        except Error as e:
            print(f"Error: {e}")
            raise

    @staticmethod
    def get_programs(**filter) -> Iterator[Program]:
        try:
            query = SSIS.SELECT_PROGRAMS_QUERY

            # Build dynamic WHERE clause based on provided filters
            if filter:
                params = []
                conditions = []

                for column, value in filter.items():
                    conditions.append(f"{column} LIKE %s")
                    params.append(f"%{value}%")

                query += " WHERE " + " OR ".join(conditions)

                return SSIS.__get_entites(f"{query} ORDER BY code", Program, tuple(params))

            return SSIS.__get_entites(f"{query} ORDER BY code", Program)
        
        except Error as e:
            print(f"Error: {e}")
            raise

    @staticmethod
    def get_students(**filter) -> Iterator[Student]:
        try:
            query = SSIS.SELECT_STUDENTS_QUERY

            # Build dynamic WHERE clause based on provided filters
            if filter:
                params = []
                conditions = []

                for column, value in filter.items():
                    conditions.append(f"{column} LIKE %s")
                    params.append(f"%{value}%")

                query += " WHERE " + " OR ".join(conditions)

                return SSIS.__get_entites(f"{query} ORDER BY id", Student, tuple(params))

            return SSIS.__get_entites(f"{query} ORDER BY id", Student)
        
        except Error as e:
            print(f"Error: {e}")
            raise

    @staticmethod
    def delete_college(college_code) -> None:
        try:
            SSIS.__delete_entity(SSIS.DELETE_COLLEGE_QUERY, college_code)
        
        except Error as e:
            print(f"Error: {e}")
        
    @staticmethod
    def delete_program(program_code) -> None:
        try:
            SSIS.__delete_entity(SSIS.DELETE_PROGRAM_QUERY, program_code)
        
        except Error as e:
            print(f"Error: {e}")

    @staticmethod
    def delete_student(student_id) -> None:
        try:
            SSIS.__delete_entity(SSIS.DELETE_STUDENT_QUERY, student_id)
        
        except Error as e:
            print(f"Error: {e}")

    @staticmethod
    def edit_college(college: College) -> None:
        try:
            SSIS.__edit_entity(SSIS.UPDATE_COLLEGE_QUERY, (college.name, college.code))
        
        except Error as e:
            print(f"Error: {e}")
            raise
    
    @staticmethod
    def edit_program(program: Program) -> None:
        try:
            SSIS.__edit_entity(SSIS.UPDATE_PROGRAM_QUERY, (program.name, program.college, program.code))
        
        except Error as e:
            print(f"Error: {e}")
            raise

    @staticmethod
    def edit_student(student: Student) -> None:
        try:
            SSIS.__edit_entity(SSIS.UPDATE_STUDENT_QUERY, (
                student.firstname, student.lastname, 
                student.year, student.gender.value, 
                student.program, student.id
            ))
        
        except Error as e:
            print(f"Error: {e}")
            raise

    @staticmethod
    def __add_entity(query: str, params: tuple[str | int, ...]) -> None:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor() as cursor: # type: ignore
                cursor.execute(query, params)
                mysql.connection.commit()
        
        except Error as e:
            mysql.connection.rollback()
            raise
    
    @staticmethod
    def __get_entity(query: str, primary_key: str, return_type: type[T]) -> Optional[T]:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor(dictionary=True) as cursor: # type: ignore
                cursor.execute(query, (primary_key,))

                if (row := cursor.fetchone()) is not None:
                    return return_type.from_db_row(row)
                return None
        
        except Error as e:
            raise
    
    @staticmethod
    def __get_entites(query: str, return_type: type[T], params: Optional[tuple] = None) -> Iterator[T]:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor(dictionary=True) as cursor:  # type: ignore
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)

                return (return_type.from_db_row(row) for row in cursor.fetchall() if row is not None)
        
        except Error as e:
            raise
    
    @staticmethod
    def __delete_entity(query: str, primary_key: str) -> None:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor(dictionary=True) as cursor: # type: ignore
                cursor.execute(query, (primary_key,))
                mysql.connection.commit()
        
        except Error as e:
            mysql.connection.rollback()
            raise
    
    @staticmethod
    def __edit_entity(query: str, params: tuple[str | int, ...]) -> None:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor() as cursor: # type: ignore
                cursor.execute(query, params)
                mysql.connection.commit()
        
        except Error as e:
            mysql.connection.rollback()
            raise