function getPersonDetails(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const result = document.getElementById("result");
    const empResult = document.getElementById("empResult");
    const table = document.getElementById("table");

    fetch(`http://127.0.0.1:8000/persons/by_name/?name=${name}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                table.classList.remove("hidden");
                let detailsString = "";
                data.forEach((person) => {
                    detailsString += `
                    <tr>
                        <td>${person.emp_id}</td>
                        <td>${person.name}</td>
                        <td>${person.salary}</td>
                        <td>${person.designation}</td>
                        <td>${person.address}</td>
                    </tr>`;
                });
                empResult.innerHTML = detailsString;
            } else {
                result.innerHTML = "No person found with the given name.";
            }
        })
        .catch((err) => {
            result.innerHTML = "Error fetching person details: " + err.message;
        });
}

function uploadFile(event) {
    event.preventDefault();

    const file = document.getElementById("file");
    const formData = new FormData();
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
        .value;
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append("file", file.files[0]);

    fetch("http://127.0.0.1:8000/upload/", { method: "POST", body: formData })
        .then((response) => response.text())
        .then((data) => {
            let result = document.getElementById("result");
            result.innerHTML =
                "<div class='center' style='color: green;'>Data Uploaded successfully</div>";
        })
        .catch((err) => {
            alert("Error: " + err.message);
        });
}
