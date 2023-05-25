
async function init() {
    let data = await getRequest("/api/users/me-student")
    let student = document.getElementById("student_data");
    let avatar = document.getElementById("student_avatar")
    student.innerHTML = data.firstname + " " + data.surname + "\n" + data.group;
    avatar.src = data.avatar;
}

init()
