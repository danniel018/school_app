from app.database import db
from sqlalchemy.dialects.mysql import INTEGER, ENUM, TINYINT
from .grades import Grades

class GradesSubjects(db.Model):
    __tablename__ = 'grades_subjects'
    grade_subject_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))
    subject_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    teacher_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    classrom = db.Column(db.String(5), nullable = True)
    
    

    
    