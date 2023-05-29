
async function choosePage(){
    const token = localStorage.getItem('Token')
    if (token !== "null") {
        let data = await getRequest("/api/users/me")
        let role = data.role
        let nextPage = "/me";

        if (role === "Worker") {
            nextPage = "/canteen-worker"
        }
        window.location.href = nextPage;
    }
}

choosePage()
