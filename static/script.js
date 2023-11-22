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
        result.innerHTML = JSON.stringify(data);
    })
    .catch(err => {
        result.innerHTML = "Error fetching person details: " + err.message;
    });
}
