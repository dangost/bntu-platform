let global_teachers = []
let global_groups = []


async function init() {
    let slitted_values = document.location.toString().split('/');
    let dep_id = slitted_values[slitted_values.length - 1];

    let data = await getRequest(`/api/divisions/groups?department=${dep_id}`)

    let dep_avatar = document.getElementById("dep_avatar");
    let dep_name = document.getElementById("dep_name");
    let dep_short = document.getElementById("dep_short");
    let dep_description = document.getElementById("dep_description");

    dep_avatar.src = data.departments.avatar !== null ? data.departments.avatar : "/img/bntu_main.png";
    dep_name.innerHTML = data.departments.name;
    dep_short.innerHTML = data.departments.shortname;
    dep_description.innerHTML = data.departments.description;

    global_groups = data.groups;
    global_teachers = await getRequest(`/api/users/dep-teachers/${dep_id}`)

    output_students();
}


function output_students() {
    let blocks = "";
    for (let i = 0; i < global_groups.length; i++) {
        let group = global_groups[i];
        let group_id = group.id;
        let leader_fullname = group.leader.firstname + " " + group.leader.surname;
        let course = group.leader.course + " курс";
        let phone = group.leader.phone_number;
        let avatar = group.leader.avatar;
        blocks += `
        <div class="container text-center" style="border: solid 1px; margin-top: 25px">
<div class="row g-5">
<div class="row-cols-1">

<table>
<tr>
<td><a href="/group/${group_id}"><h5><b>${group_id}</b></h5></a></td>
<td><h6>${course}</h6></td>
<td><h6>${leader_fullname}</h6></td>
<td><h6>${phone}</h6></td>
<td><img src="${avatar}" style="max-width: 100px"></td>
</tr>
</table>
</div>
</div>
`
    }

    let groups_container = document.getElementById("groups");
    groups_container.innerHTML = blocks;
}


function output_teachers() {
    let blocks = "";
    for (let i = 0; i < global_teachers.length; i++) {
        let teacher = global_teachers[i];

        let job_title = teacher.job_title
        let fullname = teacher.firstname + " " + teacher.surname;
        let phone = teacher.phone_number;
        let avatar = teacher.avatar;
        blocks += `
        <div class="container text-center" style="border: solid 1px; margin-top: 25px">
<div class="row g-5">
<div class="row-cols-1">

<table>
<tr>
<td><h6>${job_title}</h6></td>
<td><h6>${fullname}</h6></td>
<td><h6>${phone}</h6></td>
<td><img src="${avatar}" style="max-width: 100px"></td>
</tr>
</table>
</div>
</div>
`
    }

    let groups_container = document.getElementById("groups");
    groups_container.innerHTML = blocks;
}


function buttonTrigger() {
    let button = document.getElementById("switch_button");
    if (button.innerHTML === "Преподаватели") {
        button.innerHTML = "Группы";
        output_teachers()
        return;
    }
    if (button.innerHTML === "Группы") {
        button.innerHTML = "Преподаватели";
        output_students()
    }
}



init()
