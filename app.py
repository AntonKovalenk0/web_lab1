from flask import Flask, render_template, request, json, jsonify
from flask_restful import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from controler import *
import smtplib
from flask import Flask, render_template, request, jsonify, session as t_s
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from email.message import EmailMessage

app = Flask(__name__)
api = Api(app)
app.secret_key = 'web'
engine = create_engine('postgresql://postgres:1234@localhost/db11', echo=True)
CORS(app, support_credentials=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        data = request.json
        if data['email'] == "" or data['password'] == "":
            return jsonify({'message': 'Invalid data'})
        temp = session.query(User).filter(User.email == data['email']).first()
        if temp.password == data['password']:
            return jsonify({'message': 'Success', 'id': temp.id, 'status': temp.status, 'firstname': temp.firstname,
                            'email': temp.email, 'lastname': temp.lastname})
    except Exception as e:
        return jsonify({'message': 'User not found'})
    return jsonify({'message': 'Enter correct name/password'})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'error'})


@app.errorhandler(405)
def page_not_found(e):
    return jsonify({'message': 'error'})


@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    try:
        data = request.json
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        if first_name == '' or last_name == '' or email == '' or password1 == '' or password2 == '':
            return jsonify({'message': 'Invalid Data'})
        if password1 != password2:
            return jsonify({'message': 'Different passwords'})

        if session.query(User).filter(User.email == data['email']).first() != None:
            return jsonify({'message': 'Username Occupied'})
        temp_user = User(firstname=first_name, lastname=last_name, email=email, password=password1)
        session.add(temp_user)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/main')
def menu():
    if ss['email']:
        temp = session.query(User).filter(User.email == ss['email']).first()

        return render_template('index.html', status=temp.status, email=temp.email)
    else:
        return render_template('login.html')


@app.route('/add_course', methods=['POST'])
def add_course():
    try:
        data = request.json
        name = data['name']
        description = data['description']
        if name == '' or description == '':
            return jsonify({'message': 'Invalid Data'})

        temp_course = Course(name=name, description=description)
        session.add(temp_course)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})

@app.route('/delete_course', methods=['POST'])
def delete_course():
    try:
        data = request.json
        name = data['name']
        temp1 = session.query(Course).filter(Course.name == name).first()
        if name == '':
            return jsonify({'message': 'Invalid Data'})

        # temp_course = Course(name=name, description=temp1.description)
        session.delete(temp1)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})

@app.route('/profile')
def prof():
    temp = session.query(User).filter(User.email == ss['email']).first()
    return jsonify({'message': 'Success', 'status': temp.status, 'firstname': temp.firstname,'lastname': temp.lastname,
                    'email': temp.email})


@app.route('/show_course', methods=['POST'])
def show_course():
    try:
        courses = session.query(Course).filter().all()
        if len(courses) >= 1:
            return jsonify(course_list=[e.serialize() for e in courses])
        return jsonify({'message': 'Error'})
    except Exception as e:
        return jsonify({'message': 'Error'})

# @app.route('/show_prof', methods=['POST'])
# def show_course():
#     try:
#         users = session.query(User).filter().all()
#         if len(users) >= 1:
#             return jsonify(course_list=[e.serialize() for e in users])
#         return jsonify({'message': 'Error'})
#     except Exception as e:
#         return jsonify({'message': 'Error'})
# #
#
if __name__=="__main__":
    app.run(debug=True)
#     api.add_resource(AddCourse, '/teach/course')
#     api.add_resource(UpdateCourse, '/teach/course/<int:id>')
#     api.add_resource(GetCourse, '/course/<int:id>')
#     api.add_resource(DeleteCourse, '/course/<int:id>')
#
#     api.add_resource(Addteacher, '/teach')
#     api.add_resource(AddStudent, '/stud')
#     api.add_resource(UpdateTeacher, '/teach/<int:id>')
#     api.add_resource(UpdateStudent, '/stud/<int:id>')
#     api.add_resource(DeleteTeacher, '/teach/<int:id>')
#     api.add_resource(DeleteStudent, '/stud/<int:id>')
#     api.add_resource(GetTeacher, '/teach/<int:id>')
#     api.add_resource(GetStudent, '/stud/<int:id>')
#     api.add_resource(GetAllStud, '/allst')
#
#     api.add_resource(AddRequest, '/request')
#     api.add_resource(GetRequest, '/request/<int:id>')
#     api.add_resource(UpdateReq, '/request/<int:id>')

'''
 {
     "firstname": "Anton",
     "lastname": "Kovalenko",
     "password": "assddsd"
 }


 {
     "name": "Math",
     "owner_id": "7",
     "students_of_course": "5",
     "status": "1"
 }


 {
     "course_id":"1",
     "student_id":"2",
     "status":"no"
 }
'''