function displayUsers() 
{
    const request = new XMLHttpRequest();
    request.open("GET", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    request.send();

    function processData() {
        const response = JSON.parse(request.response);
        response.data.forEach(element => {
            var user_col = `
                <div class="row" style="height: 5%;">
                <div class="col h-100">
                    <div class="d-flex align-items-center h-100">
                        <img class="rounded-circle border img-fluid h-100" alt="avatar1"
                            src="https://i1.sndcdn.com/avatars-000641813667-7kcrxa-t500x500.jpg" />
                        <p class="h5 ignis" style="padding-left: 3%;">${element.username}</p>
                        <p class="h5 ignis ml-auto mr-3">Status: ${element.status}</p>
                        <button class="btn btn-primary mr-3" onclick=unbanUser(${element.user_id})>Unban</button>
                        <button class="btn btn-warning mr-3" onclick=banUser(${element.user_id})>Ban</button>
                        <button class="btn btn-danger" onclick=deleteUser(${element.user_id})>Delete</button>
                    </div>
                </div>
                </div>
                <hr class="solid">`;
                if(element.status.valueOf() != "Admin") document.getElementById("users_list").insertAdjacentHTML('beforeend', user_col);
        });
    }
}

function banUser(user_id)
{
    const request = new XMLHttpRequest();
    request.open("DELETE", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "ban",
        "user_id": user_id
    }

    request.send(JSON.stringify(data));

    function processData() {
        if(request.status != 200) console.log(request.response);
    }
}

function unbanUser(user_id)
{
    const request = new XMLHttpRequest();
    request.open("DELETE", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "unban",
        "user_id": user_id
    }

    request.send(JSON.stringify(data));

    function processData() {
        if(request.status != 200) console.log(request.response);
    }
}

function deleteUser(user_id)
{
    const request = new XMLHttpRequest();
    request.open("DELETE", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "delete",
        "user_id": user_id
    }

    request.send(JSON.stringify(data));

    function processData() {
        if(request.status != 200) console.log(request.response);
    }
}