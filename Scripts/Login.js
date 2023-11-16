function login() 
{
    const request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "login",
        "email": document.getElementById("email").value,
        "password": document.getElementById("password").value  
    }

    request.send(JSON.stringify(data));

    function processData() {
        const response = JSON.parse(request.response);
        const obj = JSON.parse(response.data);
        localStorage.setItem("user_id", obj.user_id);
        localStorage.setItem("username", obj.username);
        localStorage.setItem("email", obj.email);

        if(obj.status.valueOf() === "Admin")  window.location.href = "./Admin.html";
        else if(request.status == 200) window.location.href = "./Home.html";
        else alert("Login failed");
    }
}