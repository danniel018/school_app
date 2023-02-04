from flask import Blueprint, request,flash, redirect, url_for, jsonify
from flask_restful import Resource
from flask_login import current_user
from http import HTTPStatus
from marshmallow import ValidationError
from datetime import date
from json import JSONEncoder
from webargs import fields 
from webargs.flaskparser import use_kwargs
from sqlalchemy import func 
from app.schemas.grades import GradesSchema,EventsSchema,\
    ChildrenSchema,GradesSubjectsSchema, AnnouncementsSchema
from app.models.grades import Grades, Events,Children,GradesSubjects,\
    Announcements, childrenGradesGroups, AnnouncementsChildren
from app.database import db
from ..teachers.views import teachers


api = Blueprint('api',__name__, url_prefix='/api',template_folder='templates')
#grades_schema = EventsSchema(many=True, only=('name','grades'))
grades_schema = ChildrenSchema(many=True, exclude=('email','active'))
#grades_schema.grades.dump_only ('event',#)
event_schema = EventsSchema()
grade_schema = GradesSchema()
grades_subject_schemas = GradesSubjectsSchema(many=True)
announcements_schema = AnnouncementsSchema()
class GroupGrades(Resource):
    def get(self,subject_id):

        #grades = Events.grades_by_group(subject_id)
        grades = Children.grades_by_group(subject_id) 
        
        return grades_schema.dump(grades),HTTPStatus.OK

class ClassChildren(Resource):
    def get(self,subject_id):

        #grades = Events.grades_by_group(subject_id)
        grades = Children.by_class(subject_id) 
        
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


class AnnouncementsResource(Resource):
    def post(self): 

        if not request.form.get('class'):
            #try:
            print('df')
            new_announcement = Announcements(date=date.today(),
                teacher_id=current_user.id,filelink='gcp.cloudstorage.com')#complete
            db.session.add(new_announcement)
            new_announcement_id = db.session.query(func.last_insert_id()).first()[0]
            grade_groups = GradesSubjects.subjects_by_teacher(current_user.id)

            # new_announcement.grade_groups = [ _ for _ in grade_groups]
            
            for x in grade_groups:
                children = childrenGradesGroups.children_by_grade_group(x.grade_group_id)
                for i in children:
                    print('announcement: ',new_announcement_id,
                        'child_id: ',i.child_id,'group_id: ',x.grade_group_id)
                    # announcement_children = AnnouncementsChildren(announcement_id = new_announcement_id,
                    # child_id = )
            # print('skdjfhksjd')      
            # db.session.add(new_announcement)
            # db.session.commit() 

            return {'message':'new announcement created'},HTTPStatus.CREATED
        # except Exception as e:
            #     print(e)
            #     db.session.rollback()
            #     return {'message':'server error'},HTTPStatus.BAD_REQUEST

            
        else:
            print('class')
            # data = request.files.get('file')

            # print(data.filename)


        
        # data = request.form.get('radio1')
        # print(data)
        # print('hello madafaka')
        # announcement_date = date.today()
        # if int(data) == 1:
        #     parents = request.form.get('parents_select')
        #     if parents == 0:
        #         "logic"
        #     else:
        #         student = request.form.get('student_select')
        # else:
        #     announcement = {}
        #     announcement['date'] = announcement_date
        #     announcement['teacher_id'] = current_user.id
        #     announcement['filelink'] = 'www.skdfhksjdhfk.com'
        #     announcement = JSONEncoder(announcement)

        #     try:
        #         new_announcement = announcements_schema.load(data=announcement)
        #     except ValidationError as e:
        #         print(e.messages)
        #         return e.messages,HTTPStatus.BAD_REQUEST
            
        #     try: ##### try this insert random children in missing group
        #         new = Announcements(**new_announcement)
        #         subjects = GradesSubjects.subjects_by_teacher(current_user.id)  
        #         new.grade_groups = [x for x in subjects]
        #         db.session.add(new)
        #         db.session.commit()
        #     except Exception as e:
        #         print(e)
        #         db.session.rollback()

        return redirect(url_for('teachers.announcements'))
        