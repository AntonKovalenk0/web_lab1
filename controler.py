
from models import *


from app import session

from flask import Response, request, jsonify, json
from flask_restful import Resource, Api

#from main import work_session


from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from app import *
from sqlalchemy.ext.declarative import DeclarativeMeta




class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class AddCourse(Resource):
    def post(self):
        data = request.json
        try:
            course = Course(data["name"],data["owner_id"],data["students_of_course"],data["status"])
            session.add(course)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class UpdateCourse(Resource):
    def put(self, id):
        data = request.json
        try:
            course1 = session.query(Course).get(id)
            if "name" in data:
                course1.name = data["name"]
            if "owner_id" in data:
                course1.owner_id = data['owner_id']
            if "students_of_course" in data:
                course1.students_of_course = data["students_of_course"]
            if "status" in data:
                course1.status = data["status"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )



class GetCourse(Resource):
    def get(self, id):
        course = session.query(Course).get(id)
        if course:
            return Response(
                response=json.dumps(course, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )
class DeleteCourse(Resource):
    def delete(self, id):
        course = session.query(Course).filter(Course.id==id).delete()
        session.commit()
        if course:
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )


class SignUpUser(Resource):
    def post(self):
        data = request.json
        try:
            user = User(data["username"], data["password"])
            if session.query(User).filter(User.email == user.email).all() \
                    and session.query(User).filter(User.username == user.username).all():
                return Response(
                    response=json.dumps({"message": "user already created"}),
                    status=405,
                    mimetype="application/json"
                )
            user.password = generate_password_hash(data["password"])
            session.add(user)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "wrong input"}),
                status=404,
                mimetype="application/json"
            )