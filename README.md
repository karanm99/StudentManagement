# StudentManagement
StudentManagement - A Flask application to perform CRUD operations on Student, StudentClass using POSTgreSQL



#Technologies Used : 
Python 2.7, webapp2 framework HTML, CSS, Jquery, Bootstrap, GCP datastore
GCP appengine for deployment

#Folder Structure:

- #models.py : It contains our models of SQLAlchemy entity for POSTgresql 
- #template : It contains all the view files basically HTML files
    - courses.html  : Course View Page
    - HomePage.html : HomePage for adding course and students
- #handler.py : It is core of the web application which contains all the handlers which serve each an every request


API's Documentations :
https://app.swaggerhub.com/apis/karanm99/StudentManagement/1.0.0


Pylint's Executions to make sure code follow PEP8 Compliant : 
    - pylint --load-plugins pylint_flask_sqlalchemy "filename"

