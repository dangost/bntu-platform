
async function init() {
    let slitted_values = document.location.toString().split('/');
    let groupId = slitted_values[slitted_values.length - 1];

    let data = await getRequest(`/api/divisions/groups/${groupId}`)
    let group_id = document.getElementById("groupname");
    let group_id_lower = document.getElementById("group_id")

    let faculty = document.getElementById("user_faculty")
    let department = document.getElementById("user_department")
    let course = document.getElementById("user_course")

    group_id.innerHTML = data.id;
    group_id_lower.innerHTML = data.id;

    faculty.innerHTML = `<a href="/faculty/${data.faculty_id}">${data.faculty_short}</a>`;
    department.innerHTML = `<a href="/departments/${data.dep_id}">${data.dep_short}</a>`;
    course.innerHTML = data.course;

    let blocks = "<tr>\n" +
        "<td colspan=\"2\" class=\"identical\">ID</td>\n" +
        "<th scope=\"col\">Имя фамилия</th>\n" +
        "<th scope=\"col\">Телефон</th>\n" +
        "</tr>";
    for (let i = 0; i < data.students.length; i++) {
        let student = data.students[i];
        blocks += `
<tr>
<th colspan="2" scope="row">${student.student_id}</th>
<td>${student.firstname} ${student.surname}</td>
<td>${student.phone_number}</td>
</tr>
        `;

    }

    let table_part = document.getElementById("group_students");
    table_part.innerHTML = blocks;

}

init()