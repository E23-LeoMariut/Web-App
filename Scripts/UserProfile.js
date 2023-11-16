function onEdit() 
{
    document.getElementById("username").disabled = false;
    document.getElementById("phone").disabled = false;
    document.getElementById("descr").disabled = false;
    document.getElementById("savebtn").disabled = false;
    document.getElementById("editbtn").disabled = true;
}

function onSave() 
{
    document.getElementById("username").disabled = true;
    document.getElementById("phone").disabled = true;
    document.getElementById("descr").disabled = true;
    document.getElementById("savebtn").disabled = true;
    document.getElementById("editbtn").disabled = false;

    sendInfo();
}

function loadInfo()
{
    const request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "id",
        "user_id": localStorage.getItem("user_id")
    }

    request.send(JSON.stringify(data));

    function processData() {
        const response = JSON.parse(request.response);
        const obj = JSON.parse(response.data);
        document.getElementById("user_id").value = "#" + obj.user_id;
        document.getElementById("username").value = obj.username;
        document.getElementById("email").value = obj.email;
        document.getElementById("phone").value = obj.phone;
        document.getElementById("descr").value = obj.descr;
    }
}

function sendInfo()
{
    const request = new XMLHttpRequest();
    request.open("PATCH", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "id",
        "user_id": localStorage.getItem("user_id"),
        "username": document.getElementById("username").value,
        "email": document.getElementById("email").value,
        "phone": document.getElementById("phone").value,
        "descr": document.getElementById("descr").value,
    }

    request.send(JSON.stringify(data));

    function processData() {
        if(request.status != 200) console.log(request.response);
    }

    uploadImage();
}

function uploadImage()
{
    imageToB64(document.getElementById("profilePicture").files[0]);
}

function imageToB64(file) {
    const reader = new FileReader();
    reader.onloadend = saveImg;
    function saveImg() {
        document.getElementById("avatar").src = reader.result;
        sendImage(reader.result);
    };
    reader.readAsDataURL(file);
 }

function sendImage(image)
{
    const request = new XMLHttpRequest();
    request.open("PATCH", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "picture",
        "user_id": localStorage.getItem("user_id"),
        "avatar": image
    }

    request.send(JSON.stringify(data));
    function processData() {
        if(request.status != 200) console.log(request.response);
    }
}

function displayUserProfilePic() 
{
    const request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8080/api/users");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "ppicture",
        "user_id": localStorage.getItem("user_id")
    }
    request.send(JSON.stringify(data));

    function processData() {
        const response = JSON.parse(request.response);
        const obj = JSON.parse(response.data);
        if(obj.hasImage) document.getElementById("avatar").src = obj.avatar;
    }
}
