from app.database import db
from sqlalchemy.dialects.mysql import INTEGER, ENUM, TINYINT, YEAR
from datetime import datetime
 
# children_grade_groups = db.Table('children_grade_groups',
#     db.Column('id',INTEGER(unsigned=True),primary_key = True),
#     db.Column('child_id',INTEGER(unsigned=True),
#         db.ForeignKey('children.child_id') ,nullable = False),
#     db.Column('grade_group_id',INTEGER(unsigned=True),
#         db.ForeignKey('grade_groups.grade_group_id') ,nullable = False))


class Events(db.Model):
    __tablename__ = 'class_events'
    event_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    event_type = db.Column(ENUM('assignment','exam','laboratory','other'))
    name = db.Column(db.String(50),nullable = False)
    description = db.Column(db.String(100),nullable = True)
    date = db.Column(db.Date(),nullable=False)
    bimester = db.Column(TINYINT(),nullable = False)
    grade_subject_id = db.Column(INTEGER(unsigned=True),nullable = False)
    
    grades = db.relationship('Grades',back_populates = 'event')
    posted_on = db.Column(db.DateTime,default = datetime.utcnow)

    @classmethod
    def grades_by_group(cls,subject):
        return cls.query.filter(cls.grade_subject_id == subject).all()



class Grades(db.Model):
    __tablename__ = 'grades'
    grade_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    event_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('class_events.event_id') ,nullable = False)
    event = db.relationship('Events',back_populates = 'grades')
    child_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('children.child_id') , nullable = False)
    child = db.relationship('Children',back_populates = 'grades')
    grade = db.Column(db.Float(),nullable = False)
    remarks = db.Column(db.String(200),nullable = True)

    @classmethod
    def grades_by_group(cls,subject):
        return cls.query.join(Events, cls.event_id == Events.event_id)\
            .filter(Events.grade_subject_id == subject).all()


class Children(db.Model):
    __tablename__ = 'children'
    child_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(20),nullable = False)
    lastname = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(20),nullable = True)
    active = db.Column(ENUM('yes','no'),default = 'yes')
    grades = db.relationship('Grades',back_populates = 'child')
    #groups = db.relationship('GradeGroups',secondary=children_grade_groups, back_populates = 'children')
    
    @classmethod
    def grades_by_group(cls,subject):
        return cls.query.join(childrenGradesGroups).join(GradeGroups)\
            .join(GradesSubjects).filter(GradesSubjects.grade_subject_id == subject)\
            .order_by(cls.lastname).all()


class GradeGroups(db.Model):
    __tablename__ = 'grade_groups'
    grade_group_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(3),nullable = False)
    director_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    year = db.Column(YEAR,nullable = False)
    classrom = db.Column(db.String(5), nullable = True)
    #children = db.relationship('Children',secondary=children_grade_groups, back_populates = 'groups')


class GradesSubjects(db.Model):
    __tablename__ = 'grades_subjects'
    grade_subject_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))
    subject_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    teacher_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    classrom = db.Column(db.String(5), nullable = True) 

class childrenGradesGroups(db.Model):
    __tablename__ = 'children_grade_groups'
    id = db.Column(INTEGER(unsigned=True),primary_key = True)
    child_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('children.child_id'))
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))
    