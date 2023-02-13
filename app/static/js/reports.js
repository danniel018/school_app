let select = document.getElementById('class_id')
select.addEventListener('change',
    ()=> {students_data()})

let students = document.getElementById('students_id')
let btn = document.querySelector('.btn')

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