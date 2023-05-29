async function init() {
    let slitted_values = document.location.toString().split('/');
    let id = slitted_values[slitted_values.length - 1];

    let response = await getRequest(`/api/divisions/departments/${id}`)
    let faculty = response.faculty;
    let avatar = faculty.avatar !== null ? faculty.avatar : "/img/bntu_main.png"
    let block = "<div class=\"container text-center\" style=\"border: solid 1px; margin-top: 25px\">\n" +
        "  <div class=\"row g-2\">\n" +
        "    <div class=\"col-6\">\n" +
        `      <a href="/departments/${faculty.id}"><img src="${avatar}" width="400px" style="margin-top: 10px"></a> \n` +
        "    </div>\n" +
        "    <div class=\"col-6\">\n" +
        "      <div class=\"p-3\">\n" +
        `          <h5>${faculty.name}</h5>\n` +
        `          <p>${faculty.shortname}</p>\n` +
        `          <p>${faculty.description}</p>\n` +
        "      </div>\n" +
        "    </div>\n" +
        "  </div>\n" +
        "</div>"


    let mainDiv = document.getElementById("faculties")
    mainDiv.innerHTML = block;


    let departments = response.departments;
    let blocks = "";
    for (let i = 0; i < departments.length; i ++) {
        let dep = departments[i];
        let avatar = dep.avatar !== null ? dep.avatar : "/img/bntu_main.png"
        blocks += `<div class="container text-center" style="border: solid 1px; margin-top: 25px">\n` +
`<div class="row g-2">\n` +
`<div class="col-6">\n` +
`<a href="/groups/${dep.id}"><img src="${avatar}" width="200px" style="margin-top: 10px"></a>\n` +
`</div>\n` +
`<div class="col-6">\n` +
`<div class="p-3">\n` +
`<h5>${dep.name}</h5>\n` +
`<p>${dep.shortname}</p>\n` +
`<p>${dep.description}</p>\n` +
`</div>\n` +
`</div>\n` +
`</div>\n` +
`</div>`
    }

    let deps = document.getElementById("departments");
    deps.innerHTML = blocks;
}

init();