
async function load_info(){
    let teacher = parseInt (document.getElementById('teacher').innerHTML)
    let class_select = document.getElementById('class_select')
    let select_student = document.getElementById("student_select") 
    let parents = document.getElementById("parents_select")
    let doc = document.getElementById('formFile')
    let small = document.querySelector('small')
    doc.addEventListener('click',function() {this.style.borderColor = 'rgb(207,207,207)', small.innerHTML = ''})
    
    //document.querySelector('button').addEventListener('click',)
    const get_announcements = await fetch('/api/announcements/' + teacher)
    const announcements_response = await get_announcements.json()
    if (get_announcements.status !== 200){
        alert(get_announcements.status + announcements_response.message)
    }
    else {
        const announcements_section = document.getElementsByClassName('announcements_list')[0]
        //let index = 1 
        announcements_response.forEach((announcement,index) => {
            let element = document.createElement('div') 
            element.className = 'mb-4'
            element.innerHTML = `<h6 class = "announcements_list_inner">${index + 1}. ${announcement.announcement_type}</h6> 
                <p class = "announcements_list_inner"> date of issue: ${announcement.date}</p> 
                <a href="/teachers/announcement/${announcement.announcement_id}" class = "announcements_list_inner">more info</a>`
                
            announcements_section.appendChild(element)
        }); 

    } 
    const res = await fetch('/api/teachers/groups/' + teacher)
    const data_response = await res.json()
    if (res.status !== 200){
        alert(res.status + data_response.message)
    }
    else {
        for (let x of data_response){
            let option = document.createElement('option')
            option.value = x.grade_subject_id
            option.innerHTML = x.subject.name + x.grade_group.name
            class_select.appendChild(option)
        }
        class_select.addEventListener('change',function(){ load_students(select_student,class_select)}
        )
        parents.addEventListener('click',function(){
            student_select(this.value,select_student)},false)
    }

    let radio2 = document.getElementById("radio_2")
    radio2.addEventListener('click',function(){
        radio_form(1)
    },false)
    let radio1 = document.getElementById("radio_1")
    radio1.addEventListener('click',function(){
        radio_form(0)
    },false)

    let submit_btn = document.getElementById('submit_data')
    submit_btn.addEventListener('click',function() {
        validate_data(class_select,select_student,parents,doc,small,radio1,this)
    })
}

function radio_form(show){
    let form = document.getElementById("fieldset2")
    if(show == 1){
        form.hidden = false
        form.disabled = false           
    }
    else{
        form.hidden = true
        form.disabled = true
    }   
}

function student_select(value,select_student){
    if (parseInt (value) == 2){
        select_student.disabled = false        
    }
    else{
        select_student.disabled = true
    }
   
}

async function load_students(select,class_){
    while(select.firstChild){
        select.removeChild(select.lastChild)

    }
    const res = await fetch('/api/gradesubject/children/' + class_.value)//change url to list of students
    const data_response = await res.json()
    if (res.status !== 200){
        alert(res.status + data_response.message)
    }
    else {
        for (let x of data_response){
            let option = document.createElement('option')
            option.value = x.child_id
            option.innerHTML = x.name + ' '+ x.lastname
            select.appendChild(option)
        }
    }
}

async function validate_data(class_,student,parents,doc,small,all_parents_radio,submit){ 
    
    if(!doc.value){
        // console.log('no file')
        doc.style.borderColor = 'red'
        small.innerHTML = '*please attach a file'
        return
    }
    else if(doc.value && (doc.files[0].size/1024) > 2000){
        alert('file is too heavy, please upload a file of  up to 2Mb size')
        return
    }
    if (parseInt(class_.value) == 0 && !all_parents_radio.checked ){
        alert ('please Select a class!')
        return
    }
    submit.innerHTML = 'Generating...'
    submit.disabled = true
    console.log('request sent')
    let reason = document.getElementById('reason_id') 
    console.log(reason.value)
    const data = new FormData()
    data.append('file',doc.files[0])
    data.append('reason',reason.value)
        
    if (!all_parents_radio.checked){
            
        let grade_subject = class_.value
        data.append('class',grade_subject)

        if (parseInt(parents.value) == 2){
            data.append('student',student.value)
        }
            
    }
    for (var pair of data.entries()) {
        console.log(pair[0]+ ', ' + pair[1]);  
    }
    const res = await fetch('/api/announcements',{  
        method:'POST',
        body:data,
    })
    const data_response = await res.json()
    res.status == 201? alert('Announcement successfully generated!'):
    alert('there was an error generating the announcement :(')
    location.reload()
    // console.log(res.status)
    // console.log(data_response.message)

    
    
}