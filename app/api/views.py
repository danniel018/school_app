from flask import Blueprint, request,flash
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from app.schemas.grades import GradesSchema,EventsSchema,ChildrenSchema,GradesSubjectsSchema
from app.models.grades import Grades, Events,Children,GradesSubjects
from app.database import db


api = Blueprint('api',__name__, url_prefix='/api',template_folder='templates')
#grades_schema = EventsSchema(many=True, only=('name','grades'))
grades_schema = ChildrenSchema(many=True, exclude=('email','active'))
#grades_schema.grades.dump_only ('event',#)
event_schema = EventsSchema()
grade_schema = GradesSchema()
grades_subject_schemas = GradesSubjectsSchema(many=True)
class GroupGrades(Resource):
    def get(self,subject_id):

        #grades = Events.grades_by_group(subject_id)
        grades = Children.grades_by_group(subject_id) 
        
        return grades_schema.dump(grades),HTTPStatus.OK


class Event(Resource):
    def get(self,event_id):

        event_details = Events.get_by_id(event_id)  
        event = event_schema.dump(event_details)
        return event_schema.sort_students(event)

    def patch(self,event_id):
        data = request.get_json()
        try:
            event = event_schema.load(data = data)

        except ValidationError as e:
            print(e)
            return e.messages,HTTPStatus.BAD_REQUEST

        update_event = Events.get_by_id(event_id) 
        update_event.event_type = event.get('event_type') or update_event.event_type
        update_event.name = event.get('name') or update_event.name
        update_event.description = event.get('description') or update_event.description
        update_event.submit_date = event.get('date') or update_event.submit_date

        update_event.save()

        flash('Event updated successfully!',category='success')
        return  HTTPStatus.OK
    
        
        # event_details = Events.get_class_event(event)  
        # return event_schema.dump(event_details)

class Grade(Resource):

    def patch(self,grade_id):
        grade_data = request.get_json()
        print(grade_data)

        try:
            grade = grade_schema.load(data=grade_data)

        except ValidationError as e:
            print(e)
            return e.messages,HTTPStatus.BAD_REQUEST
        
        
        update_grade = Grades.get_by_id(grade_id) 
        update_grade.grade = grade.get('grade') or update_grade.grade
        update_grade.remarks = grade.get('remarks') or update_grade.remarks
        update_grade.save()

        flash('Grade updated successfully!',category='success')
        return  HTTPStatus.OK
       

class Teacherclasses(Resource):
    def get(self,teacher_id):

        #grades = Events.grades_by_group(subject_id)
        subjects = GradesSubjects.subjects_by_teacher(teacher_id)  
        
        return grades_subject_schemas.dump(subjects),HTTPStatus.OK