

const doAuthFetch = async (url, config, access_token, removeCookies) => {

    if('headers' in config){
        config.headers.Authorization = `Bearer ${access_token}`
    } else {
        config.headers = {
            Authorization: `Bearer ${access_token}`
        }
    }

    const data = await fetch(url, config)
    .then(async response => {
        const data = await response.json();

        if(response.status === 401){
            removeCookies("fastapp_token")
            window.location.replace("/login");
            return null;
        }
        if(!response.ok) {
            console.error("Request Error: ", data.message);
            return null;
            // TODO: Register Error
        }
        
        return data;
    })
    .catch(error => {
        console.error(error)
        return null;
    });

    return data;
}

export {doAuthFetch};