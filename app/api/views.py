from flask import Blueprint
from flask_restful import Resource
from http import HTTPStatus
from app.schemas.grades import GradesSchema
from app.schemas.grades import EventsSchema
from app.schemas.grades import ChildrenSchema
from app.models.grades import Grades
from app.models.grades import Events
from app.models.grades import Children


api = Blueprint('api',__name__, url_prefix='/api',template_folder='templates')
#grades_schema = EventsSchema(many=True, only=('name','grades'))
grades_schema = ChildrenSchema(many=True, exclude=('email','active'))
#grades_schema.grades.dump_only ('event',#)
grades_schema.im = 'helloween'

class GroupGrades(Resource):
    def get(self,subject):

        #grades = Events.grades_by_group(subject)
        grades = Children.grades_by_group(subject) 
        
        return grades_schema.dump(grades),HTTPStatus.OK
