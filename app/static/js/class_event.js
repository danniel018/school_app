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
        // data_response.forEach(student => {
        //     let tr = document.createElement('tr')
        //     let n = document.createElement('td')
        //     let name = document.createElement('td')
        //     let lastname = document.createElement('td')
        //     n.innerHTML = row
        //     name.innerHTML = student.name
        //     lastname.innerHTML = `<a href='/students/${student.child_id}'>${student.lastname}</a>`
        //     tr.appendChild(n)
        //     tr.appendChild(lastname)
        //     tr.appendChild(name)
        //     data_response[row - 1].grades.forEach(grade => {
        //         let td = document.createElement('td')
        //         td.innerHTML = grade.grade
        //         tr.appendChild(td)
        //     })
        //     body.appendChild(tr)
        //     row ++
        // })


    }
}