from app.database import db
from sqlalchemy.dialects.mysql import INTEGER, ENUM
# from.grades import Grades

# class children(db.Model):
#     __tablename__ = 'children'
#     child_id = db.Column(INTEGER(unsigned=True),primary_key = True)
#     name = db.Column(db.String(20),nullable = False)
#     lastname = db.Column(db.String(20),nullable = False)
#     email = db.Column(db.String(20),nullable = True)
#     active = db.Column(ENUM('yes','no'),default = 'yes')
#     grades = db.relationship('Grades',back_populates = 'child')
    
