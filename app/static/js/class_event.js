function load_event(){
    let event_id = parseInt (document.getElementById("event").innerHTML)
    set_data(event_id)

}

async function set_data(event_id){
    const res = await fetch('/api/events/' + event_id)
    const data_response = await res.json()

    if (res.status !== 200){
        console.log(res.status + data_response.message)
    }
    
    else{
        let task = document.querySelector('h3')
        let card = document.getElementsByClassName("card-body")
        task.innerHTML = data_response.name
        card[0].innerHTML = `<div><h6 class="text">type:</h6> <p class="text">${data_response.event_type}</p></div>
            <div><h6 class="text">name:</h6> <p class="text">${data_response.name}</p></div>
            <div><h6 class="text">Description:</h6> <p class="text">${data_response.description}</p></div>
            <div><h6 class="text">Submit date:</h6> <p class="text">${data_response.date}</p></div>
            <div><h6 class="text">Posted on:</h6> <p class="text">${data_response.posted_on}</p></div>`
        
        let body = document.querySelector('tbody');
        let row = 1
        data_response.grades.forEach(student => {
            tr = document.createElement('tr')
            let n = document.createElement('td')
            let name = document.createElement('td')
            let lastname = document.createElement('td')
            let grade = document.createElement('td')
            let grade_btn = document.createElement('td')
            grade_btn.className = 'btn btn-outline-light btn-sm'
            grade_btn.setAttribute('data-bs-toggle','modal')
            grade_btn.setAttribute('data-bs-target','#grademodal')
            grade_btn.innerHTML = student.grade || 'set'
            grade_btn.addEventListener('click',function (){
                modal_data(student,data_response.event_id);
            },false)
            n.innerHTML = row
            name.innerHTML = student.child.name
            lastname.innerHTML = `<a href='/students/${student.child.child_id}'>${student.child.lastname}</a>` 
            grade.appendChild(grade_btn)
            tr.appendChild(n)
            tr.appendChild(lastname)
            tr.appendChild(name)
            tr.appendChild(grade)
            body.appendChild(tr)
            row ++
        })
        let edit_event_btn = document.getElementById('edit_event')
        edit_event_btn.addEventListener('click',function(){
            edit_event(data_response)
        },false)

    }
}

function modal_data(student_data,event){
    let student = document.getElementById("student_name")
    let grade = document.getElementById("grade")
    let save_btn = document.getElementById("save_grade")
    save_btn.addEventListener('click', function () {
        set_grade(student_data,event);
    },false)
    student.innerHTML = student_data.child.name + ' ' + 
        student_data.child.lastname
    grade.value = student_data.grade

}

async function set_grade(student_data,event){
    let grade =  document.getElementById("grade")
    let remarks =  document.getElementById("remarks")
    if (grade.value.trim()=== '' || grade.value.trim() == null){
        grade.style.borderColor = 'red'  
    }
    else{
        let grade_data = {}
        grade_data.grade = parseInt (grade.value)
        grade_data.remarks = remarks.value

        console.log(grade_data)
        const res = await fetch('/api/grades/' + student_data.grade_id,{
            method: 'PATCH',
            headers: {
                'Content-Type':'application/json' 
            },
            body: JSON.stringify(grade_data)
        })
        const data_response = await res.json()

        if (res.status !== 200){
            alert(data_response.message)
        }
        
        else{
            location.reload()
        }

    }
}

function edit_event(event){
    let event_type = document.getElementById('type').value = event.event_type
    let name = document.getElementById('name')
    name.value = event.name
    let description = document.getElementById('description').value = event.description
    let submit_date = document.getElementById('submit_date')
    submit_date.value = event.date

    let save =  document.getElementById('save_event')
    save.addEventListener('click',function(){
        save_event_changes([name,submit_date],event)
    },false)
    
}

async function save_event_changes(form_values,event){

    let validated = true
    for(let form_value of form_values){
        if (form_value.value.trim()=== '' || form_value.value.trim() == null){
            form_value.style.borderColor = 'red'  
            validated = false
        } 
    }
    if (validated){
        let event_type = document.getElementById('type').value
        let description = document.getElementById('description').value
        let data = {}
        data.event_type = event_type
        data.name = form_values[0].value
        data.description = description
        data.date = form_values[1].value
        const res = await fetch('/api/events/' + event.event_id,{
            method: 'PATCH',
            headers: {
                'Content-Type':'application/json' 
            },
            body: JSON.stringify(data)       
        })
        const data_response = await res.json()
        if (res.status !== 200){
            alert(data_response.message)
        }
        
        else{
            location.reload()
        }
    }
}
        
    
