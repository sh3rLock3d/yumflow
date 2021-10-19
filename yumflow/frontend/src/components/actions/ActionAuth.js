const URL = 'http://127.0.0.1:8000/api/'



// LOGIN USER
export const login = (username, password) => {
    // Request Body
    const data = {username, password}

    let link = URL + "auth/login"
    let res = fetch(link, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => {
        
        if (response.status != 200) {
            throw new Error(response.json())
        }
        return response.json()
    })
    return res

};



// Setup config with token - helper function
export const tokenConfig = () => {
    // Get token from state
    const token = localStorage.getItem('token');

    // Headers
    const config = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // If token, add to headers config
    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }

    return config;
};

export const tokenConfigForm = () => {
    // Get token from state
    const token = localStorage.getItem('token');

    // Headers
    const config = {
        headers: {
            
        },
    };

    // If token, add to headers config
    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }

    return config;
};