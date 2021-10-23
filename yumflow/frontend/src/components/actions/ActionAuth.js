const URL = 'http://127.0.0.1:8000/api/'
import {USER_LOADED, LOGOUT_SUCCESS} from '../actions/types'
import { Context } from '../../Store'
import React, { useEffect, useContext } from 'react';

// LOGIN USER
export const login = (username, password) => {
    // Request Body
    const data = { username, password }

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

export const register = (data) => {
    let link = URL + "auth/register"
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

export const loadUser = () => {
    // User Loading
    //dispatch({ type: USER_LOADING });
    const [state, dispatch] = useContext(Context);
    fetch('/api/auth/user', tokenConfig())
        .then(response => response.json())
        .then((res) => {
            if (res['detail']){
                throw new Error('error')
            }
            dispatch({type: USER_LOADED, payload: res});
        })
        .catch((err) => {
            console.log(err);
            console.log('token not valid');
            //todo       dispatch({type: AUTH_ERROR,});
            localStorage.removeItem('token');
        });
}

export const logout = (dispatch) => {
    let link = '/api/auth/logout/'
    let res = fetch(link, {
        method: 'POST',
        headers: tokenConfig().headers,
    })
        .then(data=>{
            if(200 <= data.status < 300) {
                dispatch({type: LOGOUT_SUCCESS, payload: data});
            } else {
                throw new Error('error')
            }
        })
        .catch(err =>{
            console.log(err);
        })
}


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