from os import abort
from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date
from app.database import db, QueriedData
from app.forms import Events


teachers = Blueprint('teachers',__name__, url_prefix='/teachers',template_folder='templates') 

@teachers.route('/home')
def home():
    

    return render_template('teachers/home.html')

@teachers.route('/classes')

def teacher_classes():
    year=2022
    y = date.today()
    
    classes = db.session.execute("SELECT gp.name,s.name,gp.grade_group_id,gs.grade_subject_id FROM "
        "grade_groups as gp JOIN grades_subjects as gs "
        "ON gp.grade_group_id = gs.grade_group_id JOIN subjects as s ON s.subject_id = gs "
        ".subject_id WHERE gs.teacher_id = :id AND gp.year = :year",{'id':current_user.id,'year':y.year})

    return render_template('teachers/classes.html',classes=QueriedData.return_rows(classes))

@teachers.route('/classes/<int:grade_subject>',methods=['GET','POST']) 
def class_info(grade_subject):

    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)
    
    form = Events()

    students = db.session.execute("SELECT c.name, c.lastname FROM children as c JOIN children_grade_groups as "
        "cg ON c.child_id = cg.child_id JOIN grade_groups as gg ON cg.grade_group_id = gg.grade_group_id "
        "JOIN grades_subjects as gs ON gg.grade_group_id = gs.grade_group_id  WHERE gs.grade_subject_id = :id",{'id':grade_subject})


    events =  db.session.execute("SELECT event_type,name,description,date FROM class_events WHERE grade_subject_id = :id "
        "AND bimester = 4 ORDER BY posted_on DESC",{'id':grade_subject})
    events = QueriedData.return_rows(events)
    week_events = []
    exams = []
    labs = []
    no_week_events = False
    for x in events:
        if (x[3]).isocalendar()[1] == date.today().isocalendar()[1]:
            week_events.append(x)
        if x[0] == 'exam':
            exams.append(x)
        elif x[0] == 'laboratory':
            labs.append(x)

    if(len(week_events) < 1):
        no_week_events = True

    if form.add_event.data and form.validate():
        print(form.event_type.data.lower())
        
        try:
            db.session.execute("INSERT INTO class_events (event_type,name,description,date,bimester,grade_subject_id) "
                "VALUES (:eve,:nam,:des,:dat,:bim,:id)",{'eve':form.event_type.data.lower(),'nam':form.name.data,
                'des':form.description.data,'dat':form.submit_date.data,'bim':4,'id':grade_subject})
            db.session.commit()
            flash("New event created",category='success')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('error adding the event',category='Danger') 
        finally:
            return redirect (url_for('teachers.class_info',grade_subject = grade_subject))

    return render_template('teachers/class_info.html',students = students, group= class_data[1], classs= class_data[2],
        events = events, week_events = week_events, exams = exams, labs = labs, nwe = no_week_events, grade_subject = grade_subject,
        form = form) 

@teachers.route('/classes/<int:grade_subject>/grades')
def grades(grade_subject):


    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)

    students = db.session.execute("SELECT c.child_id, c.lastname,c.name FROM children as c JOIN children_grade_groups as "
        "cg ON c.child_id = cg.child_id JOIN grade_groups as gg ON cg.grade_group_id = gg.grade_group_id "
        "JOIN grades_subjects as gs ON gg.grade_group_id = gs.grade_group_id  WHERE gs.grade_subject_id = :id "
        "ORDER BY lastname",{'id':grade_subject}) 
    
    students = QueriedData.return_dic(students,'id','lastname','name') 


    events = db.session.execute("SELECT event_id,name FROM class_events WHERE grade_subject_id =2 AND "
        "bimester = 4 ORDER BY date",{'id':grade_subject})
    events = QueriedData.return_rows(events)
    print(events)
    for y in students:
        s_events = {}
        for x in events:
            event_ = {}
            event_['event_id'] = x[0] 
            event_['grade'] = ''
            s_events[x[1]] = event_
        y['events'] = s_events

    grades = db.session.execute("SELECT g.child_id, e.event_id, g.grade FROM grades as g JOIN class_events "
        "as e ON g.event_id = e.event_id WHERE grade_subject_id = :id",{'id':grade_subject})
    grades = QueriedData.return_rows(grades) 

    for y in students:
        for x in grades:
            if y['id'] == x[0]:
                for z in y['events'].values():
                    if z['event_id'] == x[1]:
                        z['grade'] = x[2]  
            

    print(students)

    return render_template('teachers/grades.html',grades = students, group = class_data[1], classs = class_data[2],
        events = events)


@teachers.route('/classes/<int:grade_subject>/events')
def class_events(grade_subject):

    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)

    events = db.session.execute("SELECT name,description,date,event_id FROM class_events WHERE grade_subject_id = :id "
        "AND bimester = 4 ORDER BY date",{'id':grade_subject}) 
    events = QueriedData.return_rows(events) 

   
    return render_template('teachers/events.html', group = class_data[1], classs = class_data[2], events = events,
        grade_subject = grade_subject)


@teachers.route('/classes/<int:grade_subject>/events/<int:event>')
def event(grade_subject,event):

    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)

    class_event = db.session.execute("SELECT event_type,name,description,date,posted_on FROM "
        "class_events WHERE event_id=:id",{'id':event})
    class_event = QueriedData.return_row(class_event) 

    students = db.session.execute("SELECT c.child_id, c.lastname,c.name,NULL FROM children as c JOIN children_grade_groups as "
        "cg ON c.child_id = cg.child_id JOIN grade_groups as gg ON cg.grade_group_id = gg.grade_group_id "
        "JOIN grades_subjects as gs ON gg.grade_group_id = gs.grade_group_id  "
        "WHERE gs.grade_subject_id = :id ORDER BY lastname",{'id':grade_subject}) 
    students = QueriedData.return_dic(students,'id','lastname','name','grade')

    grades = db.session.execute("SELECT child_id,grade FROM grades WHERE event_id = :event",{'event':event}) 
    grades = QueriedData.return_rows(grades)

    for x in students:
        for y in grades:
            if x['id'] == y[0]:
                x['grade'] = y[1]
                break
            
    
    print(students)
    return render_template('teachers/event.html', group = class_data[1], classs = class_data[2],
        grade_subject = grade_subject, event = class_event, students = students)