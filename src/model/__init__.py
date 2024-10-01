from __future__ import annotations

from collections.abc import Iterator
from typing import Optional, TypeVar

from mysql.connector.cursor import MySQLCursorDict
from mysql.connector import Error

from src.entities import College, Program, Student
from src import mysql

T = TypeVar("T", bound=College | Program | Student)

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
    def __get_entites(query: str, return_type: type[T]) -> Iterator[T]:
        try:
            cursor: MySQLCursorDict
            with mysql.connection.cursor(dictionary=True) as cursor: # type: ignore
                cursor.execute(query)

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