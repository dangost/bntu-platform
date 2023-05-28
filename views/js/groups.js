
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

    let blocks = "";
    for (let i = 0; i < data.groups.length; i++) {
        let group = data.groups[i];
        let group_id = group.id;
        let leader_fullname = group.leader.firstname + " " + group.leader.surname;
        let course = group.leader.course;
        let phone = group.leader.phone_number;
        let avatar = group.leader.avatar;
        blocks += `
        <div class="container text-center" style="border: solid 1px; margin-top: 25px">
<div class="row g-5">
<div class="row-cols-1">

<table>
<tr>
<td><a href="/group/${group_id}"><h5><b>${group_id}</b></h5></a></td>
<td><h6>${course} курс</h6></td>
<td><h6>${leader_fullname}</h6></td>
<td><h6>${phone}</h6></td>
<td><img src="${avatar}" style="max-width: 50px"></td>
</tr>
</table>
</div>
</div>
`
    }

    let groups_container = document.getElementById("groups");
    groups_container.innerHTML = blocks;
}

init()
