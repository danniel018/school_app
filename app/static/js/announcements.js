
async function load_info(){
    let teacher = parseInt (document.getElementById('teacher').innerHTML)
    let class_select = document.getElementById('class_select')
    let select_student = document.getElementById("student_select")
    //document.querySelector('button').addEventListener('click',)

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
        document.getElementById("parents_select").addEventListener('click',function(){
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