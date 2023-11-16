function displayPosts()
{
    const request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8080/api/posts");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "operation": "get_personal",
        "user_id": localStorage.getItem("user_id")
    }
    request.send(JSON.stringify(data));

    function processData() {
        const response = JSON.parse(request.response);
        const obj = response.data;
        obj.forEach(element => {
            let section;
            if (element.type.valueOf() === "text") {
                section = `
                    <div class="row">
                        <div class="col flex-grow-1">
                            <p class="text-white"> ${element.text} </p>
                        </div>
                    </div>`;
            }
            if (element.type.valueOf() === "image") {
                var image = element.hasImage ? element.image : "'https://images.nature.com/original/magazine-assets/d41586-023-02893-y/d41586-023-02893-y_26041780.jpg'"
                section = `
                    <div class="row">
                        <div class="col flex-grow-1">
                            <img class="img-fluid rounded mb-3"
                                src=${image}>
                        </div>
                    </div>`;
            }

            let card = `
            <!-- POST CARD ELEMENT START-->
            <div class="row m-5 d-flex justify-content-center">
                <div class="col-10">
                    <div class="embed-responsive embed-responsive-4by3 text-left blur">
                        <div class="embed-responsive-item spaced" style="overflow-y: scroll;">

                            <div class="container-fluid h-100">

                                <div class="row h-10">
                                    <div class="col h-100">
                                        <div class="d-flex align-items-center h-100">
                                            <button onclick=deletePost(${element.post_id}) class="btn btn-danger"> Delete </button>
                                            <p class="h3 ignis ml-auto" style="padding-right: 3%;">${element.username}</p>
                                            <img class="rounded-circle border img-fluid h-100" alt="avatar1"
                                                src="https://t3.ftcdn.net/jpg/05/71/08/24/360_F_571082432_Qq45LQGlZsuby0ZGbrd79aUTSQikgcgc.jpg" />
                                        </div>
                                    </div>
                                </div>

                                <hr class="solid">

                                <div class="row">
                                    <div class="col h-100">
                                        <p class="h3 ignis"> ${element.title} </p>
                                    </div>
                                </div>

                                <hr class="solid">

                                ${section}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- POST CARD ELEMENT END-->
            `;
            document.getElementById("posts_list").insertAdjacentHTML('beforeend', card);
        });
    }
}

function deletePost(post_id)
{
    const request = new XMLHttpRequest();
    request.open("DELETE", "http://localhost:8080/api/posts");
    request.setRequestHeader("Access-Control-Allow-Credentials", "true");
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = processData;

    const data = {
        "post_id": localStorage.getItem("user_id")
    }
    request.send(JSON.stringify(data));

    function processData() {
        if(request.status != 200) console.log(request.response);
    }
}