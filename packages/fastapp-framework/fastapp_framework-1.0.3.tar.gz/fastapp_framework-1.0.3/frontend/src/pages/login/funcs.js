
async function getToken(username, password){
    const data = await fetch("/api/v1/auth/token", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    })
    .then(async response => {
        const data = await response.json();
        if(!response.ok) {
            console.error("Request Error: ", data.message);
        }
        
        return data;
    })
    .catch(error => {
        console.error(error)
    });

    return data;
}

async function testToken(access_token){
    const status = await fetch("/api/v1/auth/users/me", {
        headers: {
            Authorization: `Bearer ${access_token}`
        }
    })
    .then(async response => {
        const data = await response.json();
        if(!response.ok) {
            console.error("Request Error: ", data.message);
        }

        if(data === undefined) return false;
        
        return 'name' in data
    })
    .catch(error => {
        console.error(error)
    });

    return status;
}

export {getToken, testToken};