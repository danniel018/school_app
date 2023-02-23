from os import abort
from flask import Blueprint ,make_response, render_template,flash,redirect,url_for,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date, timedelta, time, datetime
from app.database import db, QueriedData
from app.forms import Events


teachers = Blueprint('teachers',__name__, url_prefix='/teachers',template_folder='templates') 

@teachers.route('/home')
@login_required
def home():

    teacher = db.session.execute("SELECT name, lastname FROM users WHERE "
        "user_id = :uid",{'uid':current_user.id})
    teacher = QueriedData.return_row(teacher)

    today = date.today()
    week = today.isocalendar()[1]

    week_classes = db.session.execute(" SELECT s.weekday_iso,s.start,s.end FROM "
        "schedule_subjects as s JOIN grades_subjects as g ON s.grade_subject_id = "
        "g.grade_subject_id WHERE g.teacher_id = :tid",{'tid':current_user.id})
    
    week_classes  = QueriedData.return_rows(week_classes)

     
    next_classes = []
    for day in week_classes:
        daytime = datetime.fromisocalendar(today.year,week,day[0]) 
        #print(day[1])
        time_ = time.fromisoformat(day[1])
        #print(time_)
        daytime = daytime + timedelta(hours=time_.hour,minutes=time_.minute)
        if daytime > datetime.now():
            next_classes.append(daytime.strftime("%b %d %Y at %H:%M"))

    next_classes = sorted(next_classes)       

    
        

    


    return render_template('teachers/home.html', teacher = teacher, next_classes = next_classes)

@teachers.route('/classes')
@login_required
def teacher_classes():
    year=2022
    y = date.today()
    
    classes = db.session.execute("SELECT gp.name,s.name,gp.grade_group_id,gs.grade_subject_id FROM "
        "grade_groups as gp JOIN grades_subjects as gs "
        "ON gp.grade_group_id = gs.grade_group_id JOIN subjects as s ON s.subject_id = gs "
        ".subject_id WHERE gs.teacher_id = :id AND gp.year = :year",{'id':current_user.id,'year':year})

    return render_template('teachers/classes.html',classes=QueriedData.return_rows(classes))

@teachers.route('/classes/<int:grade_subject>',methods=['GET','POST'])  
@login_required
def class_info(grade_subject):

    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)
    
    form = Events()

    no_added_events = False

    students = db.session.execute("SELECT c.child_id,c.name, c.lastname FROM children as c JOIN children_grade_groups as "
        "cg ON c.child_id = cg.child_id JOIN grade_groups as gg ON cg.grade_group_id = gg.grade_group_id "
        "JOIN grades_subjects as gs ON gg.grade_group_id = gs.grade_group_id  WHERE gs.grade_subject_id = :id",{'id':grade_subject})
    students = QueriedData.return_rows(students)

    events =  db.session.execute("SELECT event_type,name,description,date FROM class_events WHERE grade_subject_id = :id "
        "AND bimester = 4 ORDER BY posted_on DESC",{'id':grade_subject})
    events = QueriedData.return_rows(events)
    if len(events) == 0:
        no_added_events = True
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
            new_event = db.session.execute("SELECT LAST_INSERT_ID()")
            new_event = QueriedData.return_one(new_event)
            print(new_event)
            for x in students:
                db.session.execute("INSERT INTO grades (event_id,child_id) VALUES (:eve, :chi)",{'eve':new_event,'chi':x[0]})
            db.session.commit()
            flash("New event created",category='success')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('error adding the event',category='danger') 
        finally:
            return redirect (url_for('teachers.class_info',grade_subject = grade_subject))

    return render_template('teachers/class_info.html',students = students, group= class_data[1], classs= class_data[2],
        events = events, week_events = week_events, exams = exams, labs = labs, nwe = no_week_events, grade_subject = grade_subject,
        form = form, nae = no_added_events) 

@teachers.route('/classes/<int:grade_subject>/grades')
@login_required
def grades(grade_subject):


    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)

    
    return render_template('teachers/grades.html', group = class_data[1], classs = class_data[2], 
        grade_subject = grade_subject)


@teachers.route('/classes/<int:grade_subject>/events')
@login_required
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
@login_required
def event(grade_subject,event):

    class_ = db.session.execute("SELECT gs.teacher_id,gg.name, s.name FROM grades_subjects as gs "
        "JOIN grade_groups as gg ON gs.grade_group_id = gg.grade_group_id JOIN subjects as "
        "s ON s.subject_id = gs.subject_id WHERE gs.grade_subject_id  = :id",{'id':grade_subject})
    class_data = QueriedData.return_row(class_) 
    
    if class_data[0] != current_user.id:
        abort(403)

    
    return render_template('teachers/event.html', group = class_data[1], classs = class_data[2],
        grade_subject = grade_subject, event = event)


@teachers.route('/announcements')
@login_required
def announcements():
    
    
    return render_template('teachers/announcements.html')


@teachers.route('/announcement/<int:announcement_id>')
@login_required
def announcement(announcement_id):

    announcement_data = db.session.execute("SELECT * FROM announcements WHERE "
        "announcement_id = :aid",{'aid':announcement_id})
    announcement_data = QueriedData.return_row(announcement_data)
 
    announcement_children = db.session.execute("SELECT g.name, c.name, c.lastname FROM "
        "announcements_children as a JOIN grade_groups as g ON a.grade_group_id = "
        "g.grade_group_id JOIN children as c ON a.child_id = c.child_id WHERE "
        "a.announcement_id = :aid",{'aid':announcement_id})

    announcement_children = QueriedData.return_rows(announcement_children)
    

    
    return render_template('teachers/announcement.html',announcement = announcement_data,
        children = announcement_children)


@teachers.route('/reports')
@login_required
def reports():

    year = 2022
    classes = db.session.execute("SELECT gp.name,s.name,gp.grade_group_id,gs.grade_subject_id FROM "
        "grade_groups as gp JOIN grades_subjects as gs "
        "ON gp.grade_group_id = gs.grade_group_id JOIN subjects as s ON s.subject_id = gs "
        ".subject_id WHERE gs.teacher_id = :id AND gp.year = :year",{'id':current_user.id,'year':year})

    classes = QueriedData.return_rows(classes)

    
    return render_template('teachers/reports.html', classes = classes)