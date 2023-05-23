function logout() {
    localStorage.setItem('Token', "null");
    window.location.href = '/';
}
