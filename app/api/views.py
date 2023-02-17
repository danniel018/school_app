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
from marshmallow.validate import OneOf 
from app.schemas.grades import GradesSchema,EventsSchema,\
    ChildrenSchema,GradesSubjectsSchema, AnnouncementsSchema, \
        AnnouncementsChildrenSchema, ReportsSchema

from app.models.grades import Grades, Events,Children,GradesSubjects,\
    Announcements, childrenGradesGroups, AnnouncementsChildren, Reports
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



class AnnouncementResource(Resource):
    
    def get(self,teacher_id):
        announcements_children_schema = AnnouncementsChildrenSchema(many=True)
        announcements_list = AnnouncementsChildren.get_by_teacher(teacher_id) 
        print(announcements_list)

        return announcements_children_schema.dump(announcements_list), HTTPStatus.OK

class AnnouncementsResource(Resource):
    
    def post(self): 
        try:
            file = request.files.get('file')
            reason = request.form.get('reason') 
            if str(reason) != 'announcement' and str(reason) != 'summons':
                raise ValueError
        
            new_announcement = Announcements(type = reason,date=date.today(),
                    teacher_id=current_user.id,filelink=f'{file.filename}-cloudstorage.com') 
            db.session.add(new_announcement)
            new_announcement_id = db.session.query(func.last_insert_id()).first()[0]

            if not request.form.get('class'):
                
                grade_groups = GradesSubjects.subjects_by_teacher(current_user.id)

                
                for x in grade_groups:
                    children = childrenGradesGroups.children_by_grade_group(x.grade_group_id)
                    for i in children:
                        print('announcement: ',new_announcement_id,
                            'child_id: ',i.child_id,'group_id: ',x.grade_group_id)
                        announcement_children = AnnouncementsChildren(announcement_id = new_announcement_id,
                        child_id =i.child_id,grede_group_id = x.grade_group_id)
                
                return {'message':'new announcement created'},HTTPStatus.CREATED 

            else:
                
                grade_subject_id = int(request.form.get('class'))
                
                if not request.form.get('student'):
                    children = Children.by_class(grade_subject_id)
                    grade_group = GradesSubjects.by_id(grade_subject_id) 
                    for x in children:
                        print('ann_id: ',new_announcement_id,'child: ',x.child_id,'group: ',grade_group.grade_group_id)
                        announcement_children = AnnouncementsChildren(announcement_id = new_announcement_id,
                        child_id =x.child_id,grede_group_id = grade_group.grade_group_id)

                    return {'message':'new announcement created'},HTTPStatus.CREATED 

                else: 
                    child_id = int(request.form.get('student'))
                    child = childrenGradesGroups.by_id(child_id)
                    print('ann_id: ',new_announcement_id,'child: ',child.child_id,'group: ',child.grade_group_id)
                    announcement_children = AnnouncementsChildren(announcement_id = new_announcement_id,
                        child_id =child.child_id,grade_group_id = child.grade_group_id)

                    return {'message':'new announcement created'},HTTPStatus.CREATED 


            #UPLOAD FILE TO CLOUD STORAGE SERVER
            #UPLOAD FILE TO CLOUD STORAGE SERVER
            #UPLOAD FILE TO CLOUD STORAGE SERVER
            
            db.session.add(announcement_children) 
            db.session.commit()

        except (ValueError,AttributeError) as e:
                print(e)
                db.session.rollback()
                return {'message':'wrong data values or keys'},HTTPStatus.BAD_REQUEST

        return redirect(url_for('teachers.announcements'))
        
class ReportsResource(Resource):

    @use_kwargs({'teacher':fields.Int(missing = None)},location = 'query')
    def get(self,teacher=None):

        if not teacher == None:
            reports_schema = ReportsSchema(many=True)
            report_list = Reports.get_by_teacher(current_user.id)         
            print(report_list)

            return reports_schema.dump(report_list),HTTPStatus.OK
    
    def post(self):
        reports_schema = ReportsSchema()
        report = request.get_json()

        try:
            new_report = reports_schema.load(data = report)

        except ValidationError as e:
            print(e)
            print(e.messages)
            return {'message':e.messages},HTTPStatus.BAD_REQUEST

        print(new_report) 
        new = Reports(**new_report)
        new.filename = 'carcassbadasssong.xlsx'
        new.save()

        return {'message':'Reporte generado!'},HTTPStatus.OK
        