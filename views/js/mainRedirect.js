async function choosePage(){
    const token = localStorage.getItem('Token')
    if (token !== "null") {
        let data = await getRequest("/api/users/me")
        let role = data.role
        let nextPage = "";
        if (role === "Student"){
            nextPage = '/student.html';
        }
        else if (role === "Teacher") {
            nextPage = "/lecturer.html";
        }
        window.location.href = nextPage;
    }
}

choosePage()
