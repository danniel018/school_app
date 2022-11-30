from app.database import db
from sqlalchemy.dialects.mysql import INTEGER, ENUM, TINYINT
# from .grades import Grades
# from datetime import datetime

# class Events(db.Model):
#     __tablename__ = 'class_events'
#     event_id = db.Column(INTEGER(unsigned=True),primary_key = True)
#     event_type = db.Column(ENUM('assignment','exam','laboratory','other'))
#     name = db.Column(db.String(50),nullable = False)
#     description = db.Column(db.String(100),nullable = True)
#     date = db.Column(db.Date(),nullable=False)
#     bimester = db.Column(TINYINT(),nullable = False)
#     grade_subject_id = db.Column(INTEGER(unsigned=True),nullable = False)
#     # grade_subject_id = db.Column(INTEGER(unsigned=True),
#     #     db.ForeignKey('grades_subjects.grade_subject_id'),nullable = False)
#     # subject = db.relationship('GradeSubjects',back_populates = 'events')
#     grades = db.relationship('Grades',back_populates = 'event')
#     posted_on = db.Column(db.DateTime,default = datetime.utcnow)