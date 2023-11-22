function getPersonDetails(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const result = document.getElementById("personDetails");

    fetch(`http://127.0.0.1:8000/persons/by_name/?name=${name}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            let detailsString = "";
            data.forEach(person => {
                detailsString += `<p><b>Name:</b> ${person.name}, Emp_Id: ${person.emp_id}, Address: ${person.address}<p/>`;
            });
            result.innerHTML = detailsString;
        } else {
            result.innerHTML = "No person found with the given name.";
        }
    })
    .catch(err => {
        result.innerHTML = "Error fetching person details: " + err.message;
    });
}


function uploadFile(event){
    event.preventDefault();

    const file = document.getElementById("file");
    const formData = new FormData();
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('file', file.files[0]);

    fetch('http://127.0.0.1:8000/upload/', {method: 'POST', body: formData})
    .then(response => response.text())
    .then(data => {
        alert(data);
    })
    .catch(err => {
        alert("Error: " + err.message)
    });
}