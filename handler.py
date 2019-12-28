#!/usr/bin/env python
"""
handler.py has different Class which deals with APIs of Student and StudentClass
"""

import logging
from flask import request, render_template
import sqlalchemy
import sqlalchemy_utils
from models import DB as db, APP as app
from models import StudentDAO
from models import StudentClassDAO
import models

db.init_app(app)

@app.route('/')
def show_all():
    """
    Fetches all the students and class from db using DAO
    and render it on UI
    :return:
    """
    try:
        studentdao_xsrf_token = models.XSRFToken.create_xsrf_token(
            message=StudentDAO.XSRF_TOKEN_MESSAGE)
        studentclassdao_xsrf_token = models.XSRFToken.create_xsrf_token(
            message=StudentClassDAO.XSRF_TOKEN_MESSAGE)
        all_students = StudentDAO.get_all_students()
        all_classes = StudentClassDAO.get_all_classes()
        logging.info("Successfully fetched data")
    except Exception as exception:  # pylint: disable=broad-except
        logging.warning("Failed to load data due to %s", exception)
    return render_template('HomePage.html', students=all_students,
                           std_class=all_classes, studentdao_xsrf_token=studentdao_xsrf_token,
                           studentclassdao_xsrf_token=studentclassdao_xsrf_token)

@app.route('/add_student', methods=['POST'])
def add_student():
    """
    POST method use to add student in the db using StudentDAO
    :return: response message along with status code
    """
    if request.method == 'POST':
        try:
            xsrf_token = request.form.get('xsrf_token')
            if not models.XSRFToken().generate_and_assert_token(
                    message=StudentDAO.XSRF_TOKEN_MESSAGE, token=xsrf_token):
                return ({'message': 'Unauthorized Request'}, 401)

            class_id = request.form.get('class_id')
            student_name = request.form.get('student_name')
            StudentDAO.add_student(class_id=class_id, student_name=student_name)
            logging.info("Student was successfully added")
            return ({'message':'Student successfully created '}, 200)
        except Exception as exception:  # pylint: disable=broad-except
            logging.error("Failed to add students due to %s", exception)
            return ({'message':'Failed to add student'}, 400)
    return ({'message': 'Bad request'}, 404)

@app.route('/delete_student', methods=['POST'])
def delete_student():
    """
    POST method to delete a existing student from db
    :return: response message along with status code
    """
    if request.method == 'POST':
        try:
            xsrf_token = request.form.get('xsrf_token')
            if not models.XSRFToken().generate_and_assert_token(
                    message=StudentDAO.XSRF_TOKEN_MESSAGE, token=xsrf_token):
                return ({'message': 'Unauthorized Request'}, 401)

            student_id = request.form.get('student_id')
            course_id = request.form.get('course_id')
            StudentDAO.delete_student(id=student_id, class_id=course_id)
            logging.info("Student deleted successfully")
            return ({'message':'Successfully deleted'}, 200)
        except Exception as exception:  # pylint: disable=broad-except
            logging.error("Failed to delete student because %s", exception)
            return {'message':'Failed to delete student'}, 400
    return ({'message': 'Bad request'}, 404)

@app.route('/update_student', methods=['PUT'])
def update_student():
    """
    PUT method to update existing student from db
    :return:response message along with status code
    """
    if request.method == 'PUT':
        try:
            xsrf_token = request.form.get('xsrf_token')
            if not models.XSRFToken().generate_and_assert_token(
                    message=StudentDAO.XSRF_TOKEN_MESSAGE, token=xsrf_token):
                return ({'message': 'Unauthorized Request'}, 401)

            student_id = request.form.get('student_id')
            course_id = request.form.get('course_id')
            student_name = request.form.get('student_name')
            StudentDAO.update_student(student_id, student_name)
            logging.info("Successfully updated the student details of course %s", course_id)
            return ({'message':'Student updated successfully'}, 200)
        except Exception as exception:  # pylint: disable=broad-except
            logging.error("Failed to updated the student details due to %s", exception)
            return ({'message':'Failed to update student'}, 400)
    return ({'message': 'Bad request'}, 404)

@app.route('/assign_students', methods=['POST'])
def assign_class_to_students():
    """
    POST method to assign student to the class
    :return: response message along with status code
    """
    if request.method == 'POST':
        req_dict = request.form.to_dict()
        response = {}
        for student_details in req_dict:
            student_id = student_details
            try:
                course_id = req_dict[student_details]
                StudentDAO.assign_class(class_id=course_id, student_id=student_id)
                logging.info("Class assigned to %s successfully", student_id)
                response[student_id] = "Class assigned successfully"
            except Exception as excpetion:  # pylint: disable=broad-except
                response[student_id] = "Failed to assign class"
                logging.error("Failed to assign class to %s due to %s", student_id, excpetion)
        return ({'message':response}, 200)

    return ({'message': 'Bad request'}, 404)
@app.route('/add_class', methods=['POST'])
def add_class():
    """
    POST method to add a class in DB using StudentClassDAO
    :return: response message along with status code
    """
    if request.method == 'POST':
        try:
            xsrf_token = request.form.get('xsrf_token')
            if not models.XSRFToken().generate_and_assert_token(
                    message=StudentClassDAO.XSRF_TOKEN_MESSAGE, token=xsrf_token):
                return ({'message': 'Unauthorized Request'}, 401)

            class_name = request.form.get('class_name')
            StudentClassDAO.add_class(class_name)
            logging.info("Successfully class added")
            return ({'message':'Class added successfully'}, 200)
        except Exception as exception:  # pylint: disable=broad-except
            logging.warning("Failed to add class due to %s", exception)
            return ({'message':'Failed to add class'}, 400)
    return ({'message': 'Bad request'}, 404)

@app.route('/update_class_details', methods=['PUT'])
def update_class_details():
    """
    PUT method to update the existing class functionality

    :return: response message along with status code
    """
    if request.method == 'PUT':
        try:
            xsrf_token = request.form.get('xsrf_token')
            if not models.XSRFToken().generate_and_assert_token(
                    message=StudentClassDAO.XSRF_TOKEN_MESSAGE, token=xsrf_token):
                return ({'message': 'Unauthorized Request'}, 401)

            class_id = request.form.get('class_id')
            class_name = request.form.get('class_name')
            class_leader_id = request.form.get('class_leader_id')
            StudentClassDAO.update_class_details(class_id=class_id, class_name=class_name,
                                                 class_leader_id=class_leader_id)
            logging.info("Successfully updated the class details")
            return ({'message':'Class details updated successfully '}, 200)
        except Exception as exception:  # pylint: disable=broad-except
            logging.error("Failed to update class details due to %s", exception)
            return ({'message':'Failed to updated class details'}, 400)

    return ({'message': 'Bad request'}, 404)
@app.route('/showCourse/<course_id>', methods=['GET'])
def display_course(course_id):
    """
    Get method to get data related to particular class
    and render it on UI for course

    :param course_id:
    :return:
    """
    if request.method == 'GET':
        try:
            studentdao_xsrf_token = models.XSRFToken.create_xsrf_token(
                message=StudentDAO.XSRF_TOKEN_MESSAGE)
            studentclassdao_xsrf_token = models.XSRFToken.create_xsrf_token(
                message=StudentClassDAO.XSRF_TOKEN_MESSAGE)
            students = StudentDAO.get_students_class_id(class_id=course_id)
            unassigned_students = StudentDAO.get_all_unassigned_students()
            selected_class = StudentClassDAO.get_class_by_id(course_id)
            leader = StudentDAO.get_student_by_id(selected_class.class_leader)
            logging.info("Successfully fetched data from db")
        except Exception as exception:  # pylint: disable=broad-except
            logging.warning("Failed to fetch due to %s", exception)
    return render_template('course.html', students=students,
                           std_class=selected_class,
                           un_student=unassigned_students,
                           studentdao_xsrf_token=studentdao_xsrf_token,
                           studentclassdao_xsrf_token=studentclassdao_xsrf_token,
                           leader=leader)

if __name__ == '__main__':

    if not sqlalchemy_utils.functions.database_exists(
            'postgres://postgres:root@localhost:5432/{0}'.format(models.DB_NAME)):
        logging.info("Database not Exists, Creating a database with name %s", models.DB_NAME)
        ENGINE = sqlalchemy.create_engine("postgres://postgres:root@localhost:5432")
        CONN = ENGINE.connect()
        CONN.execute("commit")
        CONN.execute("create database {0}".format(models.DB_NAME))
        CONN.close()
    else:
        logging.info("Database Exists.")
    db.create_all()
    app.run(debug=True)
