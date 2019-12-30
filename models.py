#!/usr/bin/env python
"""
models.py has different Class which deals with DAO of Student and StudentClass
"""

import datetime
from uuid import uuid4 as gen_uuid
from typing import NewType
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import configuration as CONFIGURATION

# new type
Uuid = NewType('Uuid', str)

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = \
    CONFIGURATION.ProductionDBServiceURL.get_production_mode_db_url()
APP.config['SECRET_KEY'] = CONFIGURATION.DB_APP_CONFIG_SECRET_KEY
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
    CONFIGURATION.DB_APP_CONFIG_SQLALCHEMY_TRACK_MODIFICATIONS

DB = SQLAlchemy(APP)
Base = declarative_base()


def uuid4():
    """
    Method to generate uuid as primary key for student and student_class
    :return: string as uuid
    """
    return str(gen_uuid())


class Student(DB.Model, Base):
    """
        This is a class for db connection with PostgreSQL.
        Attributes:
            id (int): ID of student.
            name (string): name of student.
            class_id (int): class id of student.
            created_on (datetime): created on time and date.
            updated_on (datetime): updated on time and date.
    """

    # id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    __tablename__ = 'student'
    id = DB.Column(UUID, primary_key=True, default=uuid4)
    name = DB.Column(DB.String(100))
    class_id = DB.Column(UUID, DB.ForeignKey('studentclass.id'), nullable=True, index=True)
    created_on = DB.Column(DB.DateTime)
    updated_on = DB.Column(DB.DateTime, index=False, nullable=True)

    def __init__(self, name, class_id=None, updated_on=None):
        """
        __init__ method to initialize the Student Class
        :param name:
        :param class_id:
        :param updated_on:
        """
        self.name = name
        self.class_id = class_id
        self.updated_on = updated_on
        self.created_on = datetime.datetime.now()

    @property
    def get_class_id(self):
        """
        :return: class id of object
        """
        return self.class_id

    @property
    def get_name(self):
        """
        :return: returns the name of the class
        """
        return self.name

    @property
    def get_created_on(self):
        """
        :return: returns the time of creation
        """
        return self.created_on


class StudentDAO(Student):
    """
        This is a Student data access object of class Student
        for db connection with PostgreSQL. Performs CRUD Operations
    """
    XSRF_TOKEN_MESSAGE = "StudentDAO_XSRF_TOKEN_MESSAGE"

    @staticmethod
    def add_student(class_id=None, student_name=None):
        """
        Method to add student with student_name

        :param class_id:
        :param student_name:
        :return: student object
        """
        student = None
        if student_name and class_id:
            student = Student(name=student_name, class_id=class_id)
            DB.session.add(student)
            DB.session.commit()
        elif student_name:
            student = Student(name=student_name)
            DB.session.add(student)
            DB.session.commit()
        return student


    @staticmethod
    def get_all_students():
        """
        get all student method to get all the students rows from Student table
        :return: all student rows from student table
        """
        students = Student.query.all()
        return students

    @staticmethod
    def get_student_by_id(student_id):
        """
        :param student_id:
        :return: the student object with given student_id
        """
        student = None
        if student_id:
            student = Student.query.filter_by(id=student_id).first()
            if student:
                return student
        return student

    @staticmethod
    def get_students_class_id(class_id):
        """
        :param class_id:
        :return: all the students have the with class_id as class_id
        """
        students = []
        if class_id:
            students = Student.query.filter_by(class_id=class_id).all()
            if students:
                return students
        return students

    @staticmethod
    def get_student_by_multiple_filter(**kwargs):
        """
        get student by multiple filter

        :param kwargs:
        :return:
        """
        students = None
        if kwargs:
            students = Student.query.filter_by(**kwargs).first()
            if students:
                return students
        return students

    @staticmethod
    def get_all_unassigned_students():
        """
        get_all_unassigned_students

        :return:
        """
        student_with_none = []
        student_with_none = Student.query.filter_by(class_id=None).all()
        return student_with_none

    @staticmethod
    def assign_class(class_id=None, student_id=None):
        """
        assign class to students
        :param class_id:
        :param student_id:
        :return:
        """
        if class_id and student_id:
            student = StudentDAO.get_student_by_id(student_id)
            student.class_id = class_id
            DB.session.add(student)
            DB.session.commit()

    @staticmethod
    def update_student(student_id, student_name=None):
        """
        update student with student name

        :param student_id:
        :param student_name:
        :return:
        """
        student_obj = StudentDAO.get_student_by_id(student_id)
        if student_obj:
            student_obj.name = student_name
            student_obj.updated_on = datetime.datetime.now()
            DB.session.add(student_obj)
            DB.session.commit()

    @staticmethod
    def delete_student(**kwargs):
        """
        delete existing student by searching student with
        multiple filter e.g. student_id, class_id
        :param kwargs:
        :return:
        """
        student = StudentDAO.get_student_by_multiple_filter(**kwargs)
        if student:
            classes = StudentClassDAO.get_all_class_by_leader(student.id)
            if classes:
                classes.class_leader = None
                DB.session.add(classes)
                DB.session.commit()

            DB.session.delete(student)
            DB.session.commit()


class StudentClass(DB.Model, Base):
    """
    This is a StudentClass for db connection with PostgreSQL.
    Attributes:
        id (int): ID of class.
        name (string): name of class.
        class_id (int): student id of class leader.
        created_on (datetime): created on time and date.
        updated_on (datetime): updated on time and date.
    """
    XSRF_TOKEN_MESSAGE = "StudentClassDAO_XSRF_TOKEN_MESSAGE"
    __tablename__ = 'studentclass'
    id = DB.Column(UUID, primary_key=True, index=True, default=uuid4)
    name = DB.Column(DB.String(100))
    # class_leader = DB.Column(UUID, nullable=True, index=True, Foriegn)
    class_leader = DB.Column(UUID, DB.ForeignKey('student.id'), nullable=True, index=True)
    created_on = DB.Column(DB.DateTime)
    updated_on = DB.Column(DB.DateTime, index=False, nullable=True)

    def __init__(self, name):
        """
        initialization of student class object

        :param name:
        """
        self.name = name
        self.created_on = datetime.datetime.now()

    @property
    def get_name(self):
        """
        :return: name of the class
        """
        return self.name

    @property
    def get_class_leader(self):
        """
        :return: class_leader for particular class
        """
        return self.class_leader

    @property
    def get_created_on(self):
        """
        :return: time of creation
        """
        return self.created_on


class StudentClassDAO(StudentClass):
    """
        This is a StudentClass Data access object for db connection with
        PostgreSQL and perform CRUD operations
    """

    @staticmethod
    def add_class(class_name):
        """
        To create a class with given class_name
        :param class_name:
        :return:
        """
        if class_name:
            classes = StudentClass(name=class_name)
            DB.session.add(classes)
            DB.session.commit()

    @staticmethod
    def get_all_classes():
        """
        To get all the classes from db
        :return: all classes objects
        """
        classes = StudentClass.query.all()
        return classes

    @staticmethod
    def get_class_by_id(class_id):
        """
        To get class object by id
        :param class_id:
        :return: class object
        """
        current_class = None
        if class_id:
            current_class = StudentClass.query.filter_by(id=class_id).first()
            if current_class:
                return current_class
        return current_class

    @staticmethod
    def update_class_details(class_id=None, class_name=None, class_leader_id=None):
        """
        To update the existing class details by provind various fields
        :param class_id:
        :param class_name:
        :param class_leader_id:
        :return:
        """
        class_obj = StudentClassDAO.get_class_by_id(class_id)
        if class_obj and (class_leader_id or class_name):
            if class_leader_id:
                class_obj.class_leader = class_leader_id
            if class_name:
                class_obj.name = class_name
            class_obj.updated_on = datetime.datetime.now()
            DB.session.add(class_obj)
            DB.session.commit()

    @staticmethod
    def get_all_class_by_leader(student_id):
        """
        To get all the classes by leader
        :param student_id:
        :return: class object
        """
        classes = StudentClass.query.filter_by(class_leader=student_id).first()
        return classes


class XSRFToken():
    """
    XSRF Token class uses base64 to generate a unique code for message,
    to autherize the existing API
    """

    @staticmethod
    def create_xsrf_token(message=None):
        """

        :param message:
        :return: base64 encoded token
        """
        token = base64.b64encode(message.encode('utf-8', errors='strict'))
        return token

    def generate_and_assert_token(self, message=None, token=None):
        """

        :param message:
        :param token:
        :return: Assertion of token
        """
        if not token:
            return False

        new_token = str(self.create_xsrf_token(message=message))
        if new_token == token:
            return True

        return False
