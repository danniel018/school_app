from flask import Blueprint
from flask_restful import Resource
from http import HTTPStatus
from app.schemas.grades import GradesSchema
from app.schemas.grades import EventsSchema
from app.models.grades import Grades
from app.models.grades import Events


api = Blueprint('api',__name__, url_prefix='/api',template_folder='templates')
grades_schema = EventsSchema(many=True, only=('name','grades'))

class GroupGrades(Resource):
    def get(self,subject):

        grades = Events.grades_by_group(subject)
        return grades_schema.dump(grades),HTTPStatus.OK
