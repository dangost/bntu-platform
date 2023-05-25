'use strict'


async function auth(){
    const login = document.getElementById('login_field').value;
    const password = document.getElementById('password_field').value
    const payload = {
            "login": login,
            "password": password
    };

    let response = await postRequest(
        '/api/auth/login',
        payload
    )

    if (response.status !== 200) {
        alert("Incorrect login or password")
        return
    }

    let token = response.headers.get('Authorization')
    localStorage.setItem('Token', token)
    window.location.href = '/';
}
