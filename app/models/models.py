from app.database import db
from sqlalchemy.dialects.mysql import INTEGER, ENUM, TINYINT, YEAR
from datetime import datetime
 
# announcements_children = db.Table('announcements_children',
#     db.Column('id',INTEGER(unsigned=True),primary_key = True),
#     db.Column('announcement_id',INTEGER(unsigned=True),
#         db.ForeignKey('announcements.announcement_id') ,nullable = False),
#     db.Column('grade_group_id',INTEGER(unsigned=True),
#         db.ForeignKey('grade_groups.grade_group_id') ,nullable = False),
#     db.Column('child_id',INTEGER(unsigned=True),
#         db.ForeignKey('children.child_id') ,nullable = False))
    

class DataBaseChanges:

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def discard(self):
        db.session.rollback()

class AnnouncementsChildren(db.Model):
    __tablename__ = 'announcements_children'
    id = db.Column(INTEGER(unsigned=True),primary_key = True)
    announcement_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('announcements.announcement_id'))
    child_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('children.child_id'))
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))
    announcement = db.relationship('Announcements',back_populates = 'announcement_children')
    child = db.relationship('Children',back_populates = 'announcements')
    grade_group = db.relationship('GradeGroups',back_populates = 'announcements')

    
    @classmethod
    def get_by_teacher(cls,teacher):
        return cls.query.join(Announcements).filter(Announcements.teacher_id == teacher).all()


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
    def get_by_id(cls,event):
        return cls.query.filter(cls.event_id == event).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
    

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

    @classmethod
    def get_by_id(cls,grade):
        return cls.query.filter(cls.grade_id == grade).first()
    
    @classmethod
    def by_class_student(cls,child_id,grade_subject_id):
        return cls.query.join(Events).join(GradesSubjects, 
            Events.grade_subject_id == GradesSubjects.grade_subject_id)\
                .filter((cls.child_id == child_id) & 
                        (Events.grade_subject_id == grade_subject_id)).all()
        
        
    def save(self):
        db.session.add(self)
        db.session.commit()


class Children(db.Model):
    __tablename__ = 'children'
    child_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(20),nullable = False)
    lastname = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(20),nullable = True)
    active = db.Column(ENUM('yes','no'),default = 'yes')
    grades = db.relationship('Grades',back_populates = 'child')
    announcements = db.relationship('AnnouncementsChildren',back_populates = 'child')
    reports = db.relationship('Reports',back_populates = 'child')
    
    #groups = db.relationship('GradeGroups',secondary=children_grade_groups, back_populates = 'children')
    
    @classmethod
    def grades_by_group(cls,subject):
        return cls.query.join(childrenGradesGroups).join(GradeGroups)\
            .join(GradesSubjects).filter(GradesSubjects.grade_subject_id == subject)\
            .order_by(cls.lastname).all()

    @classmethod
    def by_class(cls,grade_subject_id):
        return db.session.query(cls.child_id,cls.name,cls.lastname)\
            .join(childrenGradesGroups).join(GradeGroups)\
            .join(GradesSubjects).filter(GradesSubjects.grade_subject_id == grade_subject_id)\
            .order_by(cls.lastname).all()
    
    @classmethod
    def by_id(cls,child_id):
        return cls.query.filter(cls.child_id == child_id).first()
    
    @classmethod
    def grades_by_class(cls,child_id):
        return cls.query.\
            join(Grades).join(Events, Grades.event_id == Events.event_id).\
                filter(cls.child_id == child_id).first()
    

class GradeGroups(db.Model):
    __tablename__ = 'grade_groups'
    grade_group_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(3),nullable = False)
    director_id = db.Column(INTEGER(unsigned=True)) # Update foreign key
    year = db.Column(YEAR,nullable = False)
    classroom = db.Column(db.String(5), nullable = True)
    subjects = db.relationship('GradesSubjects',back_populates = 'grade_group')
    #children = db.relationship('Children',secondary=children_grade_groups, back_populates = 'groups')
    announcements = db.relationship('AnnouncementsChildren',back_populates = 'grade_group')

    

class GradesSubjects(db.Model):
    __tablename__ = 'grades_subjects'
    grade_subject_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))
    grade_group = db.relationship('GradeGroups',back_populates = 'subjects')
    subject_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('subjects.subject_id')) # Update foreign key
    subject = db.relationship('Subjects',back_populates = 'classes')
    teacher_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('users.user_id')) # Update foreign key
    teacher = db.relationship('Users',back_populates = 'classes')
    classroom = db.Column(db.String(5), nullable = True) 
    reports = db.relationship('Reports',back_populates = 'grade_subject')
    schedule = db.relationship('ScheduleSubjects',back_populates = 'grade_subject')


    @classmethod
    def by_id(cls,grade_subject):
        return cls.query.filter(cls.grade_subject_id == grade_subject).first()
    @classmethod
    def subjects_by_teacher(cls,teacher):
        return cls.query.filter(cls.teacher_id == teacher).all()
        

class childrenGradesGroups(db.Model):
    __tablename__ = 'children_grade_groups'
    id = db.Column(INTEGER(unsigned=True),primary_key = True)
    child_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('children.child_id'))
    grade_group_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('grade_groups.grade_group_id'))

    @classmethod
    def by_id(cls,child):
        return cls.query.filter(cls.child_id == child).first()
    
    
    @classmethod
    def children_by_grade_group(cls,grade_group):
        return cls.query.filter(cls.grade_group_id == grade_group).all()
    
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(20),nullable = False)
    lastname = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(50),nullable = False, unique = True)
    password = db.Column(db.String(256),nullable = False)
    user_type = db.Column(ENUM('teacher','parent','student'))
    bucket_name = db.Column(db.String(256),nullable = True)
    classes = db.relationship('GradesSubjects',back_populates = 'teacher')
    announcements = db.relationship('Announcements',back_populates = 'teacher')

class Subjects(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    name = db.Column(db.String(35),nullable = False)
    classes = db.relationship('GradesSubjects',back_populates = 'subject')


class Announcements(db.Model):

    __tablename__ = 'announcements'
    announcement_id = db.Column(INTEGER(unsigned=True),primary_key = True)
    announcement_type = db.Column(ENUM('announcement','summons'))
    date = db.Column(db.Date,nullable = False)
    teacher_id = db.Column(INTEGER(unsigned=True),db.ForeignKey('users.user_id'),nullable=False)
    teacher = db.relationship('Users',back_populates = 'announcements')
    announcement_children = db.relationship('AnnouncementsChildren',back_populates = 'announcement')
    filelink = db.Column(db.String(256),nullable = True)

    @classmethod
    def get_by_teacher(cls,teacher):
        return cls.query.filter(cls.teacher_id == teacher).all()
    
    def save(self):
        db.session.add(self)
        db.session.commit()



class Reports(db.Model,DataBaseChanges):

    __tablename__ = 'reports'
    report_id = db.Column(INTEGER(unsigned=True),primary_key = True)

    grade_subject_id = db.Column(INTEGER(unsigned=True),
        db.ForeignKey('grades_subjects.grade_subject_id'),nullable=False)
    grade_subject = db.relationship('GradesSubjects',back_populates = 'reports')
    
    child_id = db.Column(INTEGER(unsigned=True),
        db.ForeignKey('children.child_id'),nullable=False)
    child = db.relationship('Children',back_populates = 'reports')

    created_at = db.Column(db.DateTime(),default = datetime.utcnow)
    filelink = db.Column(db.String(256),nullable = False)

    @classmethod
    def get_by_teacher(cls,teacher):
        return cls.query.join(GradesSubjects)\
            .filter(GradesSubjects.teacher_id == teacher).all()


class ScheduleSubjects(db.Model,DataBaseChanges):
    __tablename__ = 'schedule_subjects'

    schedule_subject_id = db.Column(INTEGER(unsigned=True),primary_key = True)

    grade_subject_id = db.Column(INTEGER(unsigned=True),
        db.ForeignKey('grades_subjects.grade_subject_id'),nullable=False)
    grade_subject = db.relationship('GradesSubjects',back_populates = 'schedule')

    weekday = db.Column(ENUM('M','TU','W','TH','F'))
    weekday_iso = db.Column(TINYINT(),nullable = True)
    start = db.Column(db.String(8),nullable = True)
    end = db.Column(db.String(8),nullable = True)

    @classmethod
    def get_by_teacher(cls,teacher_id):
        return cls.query.join(GradesSubjects)\
            .filter(GradesSubjects.teacher_id == teacher_id).all()



        