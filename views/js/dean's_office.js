function sendData() {
    let teacher = document.getElementById("teacher_field").value;
    let subject = document.getElementById("subject_field").value;
    let type = document.getElementById("type").value;
    let request = {"teacher": teacher, "subject": subject, "type": type};
}