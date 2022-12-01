from marshmallow import Schema, fields, validate, post_dump


class GradesSchema(Schema):
    class Meta:
        ordered = True
    
    grade_id = fields.Int(dump_only = True)
    event = fields.Nested(lambda: EventsSchema(), dump_only = True,
        only=('name',)) 
    child = fields.Nested(lambda : ChildrenSchema(),dump_only = True,
        only=('child_id','name','lastname'))
    grade = fields.Float(required = True)
    remarks = fields.String(required=True,validate=validate.Length(max=200))


class EventsSchema(Schema):
    class Meta:
        ordered = True
    
    event_id = fields.Int(dump_only = True)
    event_type = fields.String(required=True,
        validate=validate.OneOf(('assignment','exam','laboratory','other')))
    name = fields.String(required=True,validate=validate.Length(max=50))
    description = fields.String(required=True,validate=validate.Length(max=100))
    date = fields.Date(required=True)
    bimester = fields.Integer(required = True)
    grades = fields.Nested(lambda : GradesSchema(many=True),dump_only = True,
        only=('child','grade'))
    
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
    #grades.   

    im = 'hjhg'    
   
