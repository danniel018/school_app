window.onload = load_reports()

let select = document.getElementById('class_id')
select.addEventListener('change',
    ()=> {students_data()})

let students = document.getElementById('students_id')
let btn = document.querySelector('.btn')
const alert_section =document.getElementsByClassName('alert-messages')[0]
const alert_text = document.getElementById('alert-text')
btn.addEventListener('click',()=> submit_data(select.value,students.value))

async function students_data(){
    btn.disabled = true
    while (students.childElementCount > 0){
        students.removeChild(students.lastChild)
    }
    const res = await fetch('/api/gradesubject/children/' + select.value)//change url to list of students
    const data_response = await res.json()
    if (res.status !== 200){
        alert(res.status + data_response.message)
    }
    else {
        for (let x of data_response){ 
            let option = document.createElement('option')
            option.value = x.child_id
            option.innerHTML = x.name + ' '+ x.lastname
            students.appendChild(option)
        }

    }
    if (parseInt(select.value) != 0 && res.status == 200){
        btn.disabled = false
    }
   
}

async function submit_data(class_,student){
    data={grade_subject_id:parseInt (class_),
        child_id:parseInt(student)}
   
    btn.disabled = true
    btn.innerHTML = 'Generating...'
    const post = await fetch('/api/reports',
        {method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(data)
        } 
    )
    const response = await post.json() 

    if (post.status === 201){ 
        window.scrollTo({top: 0,behavior:'smooth'})
        alert_section.hidden = false
        alert_text.innerHTML = response.message
        setTimeout(()=>{location.reload()}, 2500)
    }
    else {
        alert('there was an error generating the report :(')
        location.reload()
    }
    
}

async function load_reports (){
    let param = {'teacher':parseInt(document.getElementById('teacher').innerHTML)}
    
    let params = new URLSearchParams(param)
    const get_reports = await fetch('/api/reports?'+params)//query params
    const reports_response = await get_reports.json()
    if (get_reports.status !== 200){
        alert(get_reports.status + reports_response.message)
    }
    else {
        const reports_section = document.getElementsByClassName('current-reports')[0]
        reports_response.forEach((report,index) => {
            let element = document.createElement('div')
            let filename = report.filelink.split('reports/')[1]
            element.className = 'new_report'
            element.innerHTML = `<h6 class = "announcements_list_inner">${index + 1}. 
                Report on: ${report.child.name} ${report.child.lastname}</h6>
                <p class = "announcements_list_inner"> 
                    class: ${report.grade_subject.grade_group.name} ${report.grade_subject.subject.name}</p> 
                    <p class = "announcements_list_inner">Date: ${report.created_at}</p>
                <a href="${report.filelink}" class = "announcements_list_inner" target="_blank">${filename}</a>`
                
            reports_section.appendChild(element)
        });

    }
}