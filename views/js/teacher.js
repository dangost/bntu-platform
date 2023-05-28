async function addFile() {
    let input = document.createElement("input");
    input.type = 'file';


    input.onchange = e => {
        let file = e.target.files[0];
        let filename = file.name;
        let reader = new FileReader();
        reader.readAsDataURL(file); // this is reading as data url
       // here we tell the reader what to do when it's done reading...
       reader.onload = readerEvent => {
           let content = readerEvent.target.result; // this is the content!
           let writing = false;
           let cutBase64 = "";
           for (let i = 0; i < content.length; i++) {
               if (writing) {
                   cutBase64 += content[i];
               }
               else {
                   if (content[i] === ','){
                       writing = true;
                   }
               }
           }
            const response = postRequest(
                "/api/files/upload",
                {
                    "filename": filename,
                    "base64": cutBase64
                }
            ).then(async response => {
                let data = await response.json();
                alert(data.file_id);
                let list = document.getElementById("files")
                list.innerHTML += `<li style="margin-left: 10px" file_id="${data.file_id}"">${filename}</li>`
            })
       }

    }
    input.click();
}

async function sendPost() {
    let text = document.getElementById("post-field").value;
    let scope = document.getElementById("scope").value;
    let files = []
    let filesLi = document.getElementById("files").children
    for (let i = 0; i < filesLi.length; i++){
        files.push(Number(filesLi[i].getAttribute("file_id")));
    }

    let groups = []

    scope = scope.replaceAll(" ", "");
    groups = scope.split(",");
    for (let i = 0; i < groups.length; i++){
        groups[i] = Number(groups[i]);
    }

    await postRequest(
        "/api/posts",
        {
            "container": {
                "text": text,
                "files": files
            },
            "scope": {
                "groups": groups
            }
        }
    )
}

async function loadPosts(me) {
    let userId = me.id;

    let posts = await getRequest(
        "/api/posts/" + userId
    );
    let blocks = "";

    for (let i = 0; i < posts.length; i++)
    {
        let post = posts[i];
        let files = ""
        for (let j = 0; j < posts[i].files.length; j++)
        {
            files += `<li><a href="${posts[i].files[j].download_link}">${posts[i].files[j].filename}</a> <l>${posts[i].files[j].size} mb</l></li>`
        }

        blocks +=
            "<div class=\"stream-post\">\n" +
            " <div class=\"sp-author\">\n" +
            `     <a href=\"#\" class=\"sp-author-avatar\"><img src="${me.avatar}" alt=\"\"></a>\n` +
            `     <h6 class=\"sp-author-name\"><a href=\"#\">${me.firstname + " " + me.surname}</a></h6></div>\n` +
            " <div class=\"sp-content\">\n" +
            ` <div class=\"sp-info\">${post.date}</div>\n` +
            ` <p class=\"sp-paragraph mb-0\">${post.text}</p>\n` +
            ` ${files}\n` +
            " </div>\n" +
            " <!-- /.sp-content -->\n" +
            "                    </div>"
    }

    let postsObject = document.getElementById("posts_container");
    postsObject.innerHTML = blocks;
}

async function initMainInfo(){
    const response = await getRequest('/api/users/me-teacher');
    let userAvatar = document.getElementById("user_avatar")
    let userName = document.getElementById("username");
    let userEmail = document.getElementById("user_email")
    let userPhone = document.getElementById("user_phone")

    let job = document.getElementById("user_job_title")
    let faculty = document.getElementById("user_faculty")
    let dep = document.getElementById("user_department")

    userName.innerHTML = response.firstname + " " + response.surname;
    userAvatar.src = response.avatar;
    userEmail.innerHTML = response.email;
    userPhone.innerHTML = response.phone_number;

    job.innerHTML = response.job_title;
    faculty.innerHTML = `<a href="/facutlies/${response.faculty_id}">${response.faculty_shortname}</a>`
    dep.innerHTML = `<a href="/departments/${response.departament_id}">${response.departament_name}</a>`

    await loadPosts(response)

}

initMainInfo()