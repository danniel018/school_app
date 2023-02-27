window.onload = async () => {
    let param = {'teacher':parseInt(document.getElementById('teacher').innerHTML)}
    const classes_section = document.querySelector('section')
    let params = new URLSearchParams(param)
    const get_classes = await fetch('/api/classes?'+params)//query params
    const classes_response = await get_classes.json()
    if (get_classes.status !== 200){
        alert(get_classes.status + classes_response.message)
    }

    classes_response.forEach(class_ => { 
        let class_btn = document.createElement('a')
        class_btn.className = 'class-card '
        class_btn.innerHTML = `<h5>Class: ${class_.grade_group.name} ${class_.subject.name}</h5>
                            <h6>Classroom: ${class_.grade_group.classroom}</h6>
                            <h6>Schedule:</h6>
                            `
        class_.schedule.forEach(weekday =>{
            class_btn.innerHTML += `<p>${weekday.weekday} ${weekday.start} - ${weekday.end}</p>`
        })
        class_btn.href = '/teachers/classes/'+class_.grade_subject_id
        classes_section.appendChild(class_btn)
    });
}

