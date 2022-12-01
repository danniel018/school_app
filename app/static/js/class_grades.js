function load_grades(){
    let subject = parseInt (document.querySelector('p').innerHTML)
    set_table(subject)

}

async function set_table(subject){
    const res = await fetch('/api/grades/' + subject)
    const data_response = await res.json()

    if (res.status !== 200){
        console.log(res.status + data_response.message)
      }
    
    else{
        let header = document.getElementById("head_row")
        data_response[0].grades.forEach(column => {
            let event = document.createElement('th')
            event.setAttribute('scope','col')
            event.innerHTML = column.event.name
            header.appendChild(event)
        });
        let body = document.querySelector('tbody');
        let row = 1
        data_response.forEach(student => {
            let tr = document.createElement('tr')
            let n = document.createElement('td')
            let name = document.createElement('td')
            let lastname = document.createElement('td')
            n.innerHTML = row
            name.innerHTML = student.name
            lastname.innerHTML = `<a href='/students/${student.child_id}'>${student.lastname}</a>`
            tr.appendChild(n)
            tr.appendChild(lastname)
            tr.appendChild(name)
            data_response[row - 1].grades.forEach(grade => {
                let td = document.createElement('td')
                td.innerHTML = grade.grade
                tr.appendChild(td)
            })
            body.appendChild(tr)
            row ++
        })


    }
}