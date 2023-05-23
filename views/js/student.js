async function init() {
    let data = await getRequest("/api/users/me-student")
    let name = document.getElementById("student_name");
    let group = document.getElementById("student_group");
    let avatar = document.getElementById("avatarImage");

    name.innerHTML = data.firstname + " " + data.surname;
    group.innerHTML = data.group
    avatar.src = data.avatar;
}

init()
