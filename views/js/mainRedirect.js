
async function choosePage(){
    const token = localStorage.getItem('Token')
    if (token !== "null") {
        let data = await getRequest("/api/users/me")
        let role = data.role
        let nextPage = "/me";
        // if (role === "Student"){
        //     nextPage = '/student.html';
        // }
        // else if (role === "Teacher") {
        //     nextPage = "/teacher.html";
        // }
        window.location.href = nextPage;
    }
}

choosePage()
