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
- #configuration.py : Contains constans used for application
- #Dockerfile : contains information required for installation on docker container
- #docker-compose.yaml : Contains configuration info for docker-compose
- #requirements.txt : Contains all the required library details.


API's Documentations :
https://app.swaggerhub.com/apis/karanm99/StudentManagement/1.0.0


Pylint's Executions to make sure code follow PEP8 Compliant : 
    - (pylint --load-plugins pylint_flask_sqlalchemy "filename")


#Installation

Prerequisites : must have python3 installed

Command to execute : 
    -   pip3 install -r requirements.txt
        It will install all the required packages into systems
        
    -   After POSTgresql installation , Please create a database studentManagement (By executing below commands)
        - CREATE DATABASE studentManagement;
        - \c studentManagement
    -   Run the handler file by command :
        python3 handler.py
        

#Running The App Using Docker-compose

Please follow the below steps : 
    - #git clone https://github.com/karanm99/StudentManagement.git
    - #Install Python3, Pip3
    - #Create and activate virtual environment (prefered) 
    - #Install Docker and Docker-compose (If that is not installed)
    - #In the StudentManagement Directory Run docker-compose build
    - #then run docker-compose up ("Caution : IF its giving error, Please run it twice") :  To run the application on                            http://localhost:5000

    
        
