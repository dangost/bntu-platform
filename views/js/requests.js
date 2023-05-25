'use strict'

async function postRequest(route, payload) {
    const jsonString = JSON.stringify(payload);
    const token = localStorage.getItem('Token')
    return await fetch(
        route,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": token,
            },
            body: jsonString
        }
    )
}

 async function getRequest(route) {
     const token = localStorage.getItem('Token')
     let response =  await fetch(
         route,
         {
             method:'GET',
             headers: {
                 "Authorization": token,
             }
         }
     )

     return await response.json()
 }