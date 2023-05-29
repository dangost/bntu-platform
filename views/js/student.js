
async function loadPosts() {
    let posts = await getRequest(
        "/api/posts/feed"
    );
    let blocks = "";

    for (let i = 0; i < posts.length; i++)
    {
        let post = posts[i];
        let files = ""
        let user = posts[i].user;
        for (let j = 0; j < posts[i].files.length; j++)
        {
            files += `<li><a href="${posts[i].files[j].download_link}">${posts[i].files[j].filename}</a> <l>${posts[i].files[j].size} mb</l></li>`
        }
        blocks +=
            "<div class=\"stream-post\">\n" +
            " <div class=\"sp-author\">\n" +
            `     <a href="/users/${user.user_id}" class=\"sp-author-avatar\"><img src="${user.avatar}" alt=\"\"></a>\n` +
            `     <h6 class=\"sp-author-name\"><a href=\"#\">${user.full_name}</a></h6></div>\n` +
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


async function loadRetakes() {
    let data = await getRequest("/api/retakes/")
    let retakesTable = document.getElementById("retakes_table");
    let blocks = "<tr>\n" +
        "                        <td><strong>Предмет</strong></td>\n" +
        "                        <td><strong>Преподаватель</strong></td>\n" +
        "                        <td><strong>Форма сдачи</strong></td>\n" +
        "                        <td><strong>Срок действия</strong></td>\n" +
        "                    </tr>"
    for (let i = 0; i < data.length; i++) {
        retake = data[i];
        blocks += `
<tr>
<td>${retake.subject}</td>
<td><a href="/users/${retake.teacher_id}">${retake.teacher_fullname}</a></td>
<td>${retake.type}</td>
<td>${retake.expiration}</td>
</tr>
        `
    }
    retakesTable.innerHTML = blocks;
}



async function init() {
    let data = await getRequest("/api/users/me-student")
    let student = document.getElementById("username");
    let avatar = document.getElementById("user_avatar")

    let email = document.getElementById("user_email")
    let phone = document.getElementById("user_phone")

    let studentId = document.getElementById("student_id")
    let group = document.getElementById("user_group")
    let faculty = document.getElementById("user_faculty")
    let department = document.getElementById("user_department")
    let course = document.getElementById("user_course")


    student.innerHTML = data.firstname + " " + data.surname;
    avatar.src = data.avatar;

    studentId.innerHTML = data.student_id;
    group.innerHTML = `<a href="/group/${data.group}">${data.group}</a>`
    email.innerHTML = data.email;
    phone.innerHTML = data.phone_number;
    faculty.innerHTML = `<a href="/departments/${data.faculty_id}">${data.faculty_shortname}</a>`;
    department.innerHTML = `<a href="/groups/${data.departament_id}">${data.dep_shortname}</a>`;
    course.innerHTML = data.course;

    await loadPosts();
    await loadRetakes();
}

init()
