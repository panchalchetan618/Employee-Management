function getPersonDetails(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const result = document.getElementById("result");
    const empResult = document.getElementById("empResult");
    const table = document.getElementById("table");

    empResult.innerHTML = "";
    result.innerHTML = "";

    fetch(`http://127.0.0.1:8000/persons/by_name/?name=${name}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                result.innerHTML = "<div class='center success'>" + data.length + " Employee(s) found</div>"
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
                result.innerHTML =
                    "<div class='center danger'>No person found with the given name.</div>";
            }
        })
        .catch((err) => {
            result.innerHTML =
                "<div class='center danger'>Unable to fetch person details: " +
                err.message +
                "</div>";
        });
}

function uploadFile(event) {
    event.preventDefault();

    const file = document.getElementById("file");
    const result = document.getElementById("result");
    const formData = new FormData();
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
        .value;
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append("file", file.files[0]);
    
    result.innerHTML = "";

    fetch("http://127.0.0.1:8000/upload/", { method: "POST", body: formData })
        .then((response) => response.text())
        .then((data) => {
            result.innerHTML =
                "<div class='center success'>Data Uploaded successfully</div>";
        })
        .catch((err) => {
            result.innerHTML =
                "<div class='center danger'>Unable to upload Data: " +
                err.message +
                "</div>";
        });
}
