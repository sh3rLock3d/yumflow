import React, { useEffect, useContext } from 'react';
import { Link, Redirect } from 'react-router-dom';
import { Context } from '../../Store'
import { login } from '../actions/ActionAuth'
import {LOGIN_SUCCESS} from '../actions/types'

function Login() {
    /*
    const state = {
        username: '',
        password: '',
    };
    */
    const [state, dispatch] = useContext(Context);

    const onSubmit = (e) => {
        e.preventDefault();
        //this.props.login(this.state.username, this.state.password);
        let username = document.getElementById('LoginUsernameInput').value
        let password = document.getElementById('LoginPasswordInput').value

        login(username, password)
            .then(data => {
                console.log("success"+data)
                dispatch({type: LOGIN_SUCCESS, payload: data});
            })
            .catch((error) => {
                console.error('Error:', error);
            });

    };


    return (
        <div className="col-md-6 m-auto">
            <div className="card card-body mt-5">
                <h2 className="text-center">Login</h2>
                <form onSubmit={onSubmit}>
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            id="LoginUsernameInput"
                            className="form-control"
                            name="username"
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            id="LoginPasswordInput"
                            className="form-control"
                            name="password"
                        />
                    </div>

                    <div className="form-group">
                        <button type="submit" className="btn btn-primary">
                            Login
                        </button>
                    </div>
                    <p>
                        Don't have an account? <Link to="/register">Register</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Login;
