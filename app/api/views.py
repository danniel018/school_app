from flask import Blueprint, request,flash
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from app.schemas.grades import GradesSchema
from app.schemas.grades import EventsSchema
from app.schemas.grades import ChildrenSchema
from app.models.grades import Grades
from app.models.grades import Events
from app.models.grades import Children
from app.database import db


api = Blueprint('api',__name__, url_prefix='/api',template_folder='templates')
#grades_schema = EventsSchema(many=True, only=('name','grades'))
grades_schema = ChildrenSchema(many=True, exclude=('email','active'))
#grades_schema.grades.dump_only ('event',#)
event_schema = EventsSchema()
grades_schema = GradesSchema()
class GroupGrades(Resource):
    def get(self,subject_id):

        #grades = Events.grades_by_group(subject_id)
        grades = Children.grades_by_group(subject_id) 
        
        return grades_schema.dump(grades),HTTPStatus.OK


class Event(Resource):
    def get(self,event_id):

        event_details = Events.get_class_event(event_id)  
        return event_schema.dump(event_details)

    
        
        # event_details = Events.get_class_event(event)  
        # return event_schema.dump(event_details)

class Grade(Resource):

    def patch(self,grade_id):
        grade_data = request.get_json()
        print(grade_data)

        try:
            grade = grades_schema.load(data=grade_data)

        except ValidationError as e:
            print(e)
            return e.messages,HTTPStatus.BAD_REQUEST
        
        
        update_grade = Grades.get_by_id(grade_id) 
        update_grade.grade = grade.get('grade') or update_grade.grade
        update_grade.remarks = grade.get('remarks') or update_grade.remarks
        update_grade.save()

        flash('Grade updated successfully!',category='success')
        return  HTTPStatus.OK
       