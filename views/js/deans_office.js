async function init() {
    let me = await getRequest("/api/users/me")
    if (me.role === "Student") {
        return
    }
    if (me.role === "Teacher") {
        await initTeacherRetakes(me)
        return
    }

    contentExpired();
}


function contentExpired() {
    let block =
        "<div style=\"width: 700px;\">\n        <h3 style=\"margin-bottom: 100px;\" >К сожалению, эта страница недоступна</h3>\n    </div>"
    let container = document.getElementById("main_container")
    container.innerHTML = block;

}

async function initTeacherRetakes(me) {
    let retakes = await getRequest("/api/retakes/")
    let table_content = ""
    for (let i = 0; i < retakes.length; i++) {
        let retake = retakes[i];
        table_content +=
            `
<td>${retake.subject}</td>
<td>${retake.student_fullname}</td>
<td>${retake.type}</td>
<td>${retake.expiration}</td>
            `
    }

    let block = `
<div style="width: 700px;">
<h3 style="margin-bottom: 100px;" >На данной странице вы можете посмотреть всех студентов, взявших ведомости на ваш пересдачу ваших предметов</h3>
</div>

<form style="width: 800px;">
<table class="table">
<tbody id="retakes_table">
<tr>
<td><strong>Предмет</strong></td>
<td><strong>Студент</strong></td>
<td><strong>Форма сдачи</strong></td>
<td><strong>Срок действия</strong></td>
</tr>
${table_content}
</tbody>
</table>
</form>
    `

    let container = document.getElementById("main_container")
    container.innerHTML = block;
}


function sendData() {
    let teacher = document.getElementById("teacher_field").value;
    let subject = document.getElementById("subject_field").value;
    let type = document.getElementById("type").value;
    let payload = {"teacher": teacher, "subject": subject, "type": type};
    postRequest("/api/retakes/", payload)
    alert("Ведомость создана")
}

init()