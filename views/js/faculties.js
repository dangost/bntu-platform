async function init() {
    let blocks = ""
    let response = await getRequest("/api/divisions/faculties")
    let faculties = response.faculties;
    for (let i = 0; i < faculties.length; i++) {
        let faculty = faculties[i];
        let avatar = faculty.avatar !== null ? faculty.avatar : "/img/bntu_main.png"
        let block = "<div class=\"container text-center\" style=\"border: solid 1px; margin-top: 25px\">\n" +
            "  <div class=\"row g-2\">\n" +
            "    <div class=\"col-6\">\n" +
            `      <a href="/departments/${faculty.id}"><img src="${avatar}" width="200px" style="margin-top: 10px"></a>\n` +
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
        blocks += block;
    }

    let mainDiv = document.getElementById("faculties")
    mainDiv.innerHTML = blocks;

}

init();