let radio2 = document.getElementById("radio_2")
radio2.addEventListener('click',function(){
    radio_form(1)
},false)

let radio1 = document.getElementById("radio_1")
radio1.addEventListener('click',function(){
    radio_form(0)
},false)

function radio_form(show){
    let form = document.getElementById("fieldset2")
    if(show == 1){
        form.hidden = false
        form.disabled = false
        document.getElementById("parents_select").addEventListener('click',function(){
            select_student(this.value)},false)        
    }
    else{
        form.hidden = true
        form.disabled = true
    }
}

function select_student(value){
    let select_student = document.getElementById("student_select")
    if (parseInt (value) == 2){
        select_student.disabled = false
    }
    else{
        select_student.disabled = true

    }
    // let select_student = document.getElementById("student_select")
    // select_student.
}