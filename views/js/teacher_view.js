
async function loadPosts(me){

    let posts = await getRequest(
        "/api/posts/" + me.id
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
    let slitted_values = document.location.toString().split('/');
    let userId = slitted_values[slitted_values.length - 1];
    const response = await getRequest(`/api/users/teachers/${userId}`);

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
    faculty.innerHTML = `<a href="/departments/${response.faculty_id}">${response.faculty_shortname}</a>`
    dep.innerHTML = `<a href="/groups/${response.departament_id}">${response.departament_name}</a>`

    await loadPosts(response)

}


initMainInfo()