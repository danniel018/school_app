from marshmallow import Schema, fields, validate, post_dump


class GradesSchema(Schema):
    class Meta:
        ordered = True
    
    grade_id = fields.Int(dump_only = True)
    event = fields.Nested(lambda: EventsSchema(), dump_only = True,
        only=('name',)) 
    #event_id = fields.Int(required = True)
    child_id = fields.Int(dump_only = True)
    child = fields.Nested(lambda : ChildrenSchema(),dump_only = True,
        only=('child_id','name','lastname'))
    grade = fields.Float(required = True)
    remarks = fields.String(required=False,validate=validate.Length(max=200))

    # @staticmethod
    # def sort_parameter(dic):

    #     return dic['child']['lastname']

    # @post_dump
    # def sort_students(self,data,many):
    #     if many:
    #         # order= []
            
    #         # order.append(dict(data))
             
    #         print(type(data))
    #         order.sort(key=GradesSchema.sort_parameter)
    #         print(order)
    #         return order


class EventsSchema(Schema):
    class Meta:
        ordered = True
    
    event_id = fields.Int(dump_only = True)
    event_type = fields.String(required=True,
        validate=validate.OneOf(('assignment','exam','laboratory','other')))
    name = fields.String(required=True,validate=validate.Length(max=50))
    description = fields.String(validate=validate.Length(max=100))
    date = fields.Date(required=True)
    bimester = fields.Integer(dump_only = True)
    grades = fields.Nested(lambda : GradesSchema(many=True),dump_only = True,
        only=('child','grade','grade_id'))
    posted_on = fields.DateTime(dump_only = True) 

    @staticmethod
    def sort_parameter(dic):

        return dic['child']['lastname']

    #@post_dump
    def sort_students(self,data):
        
        data['grades'].sort(key = EventsSchema.sort_parameter)

        return data

    
class ChildrenSchema(Schema):
    class Meta:
        ordered = True
    
    child_id = fields.Int(dump_only = True)
    name = fields.String(required=True,validate=validate.Length(max=20))
    lastname = fields.String(required=True,validate=validate.Length(max=20))
    email = fields.String(required=True,validate=validate.Length(max=50))
    active = fields.String(required=True,
        validate=validate.OneOf(('yes','no')))   
    grades = fields.Nested(lambda : GradesSchema(many=True, only=('event','grade')),dump_only = True) 
    
   
class GradesSubjectsSchema(Schema):
    class Meta:
        ordered = True
    
    grade_subject_id = fields.Int(dump_only = True)
    grade_group = fields.Nested(lambda: GradeGroupsSchema( only=('grade_group_id','name',)), dump_only = True) 
    subject = fields.Nested(lambda: SubjectsSchema( only=('name',)), dump_only = True) 
    teacher = fields.Nested(lambda: UsersSchema( only=('name','lastname')), dump_only = True)
    classroom = fields.String(dump_only = True)


class GradeGroupsSchema(Schema):
    class Meta:
        ordered = True
    
    grade_group_id = fields.Int(dump_only = True)
    name = fields.String(required=True,validate=validate.Length(max=3))
    director_id = fields.Int(dump_only = True)
    year = fields.Integer(dump_only = True)
    subject_id = fields.Int(dump_only = True)
    classroom = fields.String(dump_only = True)
    subjects = fields.Nested(lambda: GradesSubjectsSchema, dump_only = True)


class SubjectsSchema(Schema):
    class Meta:
        ordered = True
    
    subject_id = fields.Int(dump_only = True)
    name = fields.String(required=True,validate=validate.Length(max=35))
    classes = fields.Nested(lambda: GradesSubjectsSchema(only=('grade_group',)), dump_only = True)

class UsersSchema(Schema):
    class Meta:
        ordered = True
    
    user_id = fields.Int(dump_only = True)
    name = fields.String(required=True,validate=validate.Length(max=20))
    lastname = fields.String(required=True,validate=validate.Length(max=20))
    email = fields.String(required=True,validate=validate.Length(max=50))
    user_type = fields.String(required=True,
        validate=validate.OneOf(('teacher','parent','student'))) 
    classes = fields.Nested(lambda: GradesSubjectsSchema(only=('grade_group',))
        ,dump_only = True)
