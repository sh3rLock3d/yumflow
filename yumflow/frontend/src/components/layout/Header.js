import React, { useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { Context } from '../../Store'
import { loadUser, logout } from '../actions/ActionAuth'

function Header() {
    const [state, dispatch] = useContext(Context);

    const isAuthenticated = state.auth.isAuthenticated
    const user = state.auth.user
    if (!isAuthenticated){
        if(localStorage.getItem('token')) {
            loadUser()
        }
    }

    const logoutUser = ()=>{
        logout(dispatch)
    }


    const authLinks = (
        <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
            <span className="navbar-text ml-3 text-white"> 
                <strong>{user ? `${user.username}` : ''}</strong>
            </span>
            <li className="nav-item active">
                <button className="nav-link btn btn-light btn-sm  text-dark" onClick={logoutUser}>
                    خروج
                </button>
            </li>
        </ul>
    );



    const guestLinks = (
        <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
            <li className="nav-item active">
                <Link to="/register" className="nav-link">
                    ثبت نام
                </Link>
            </li>
            <li className="nav-item active">
                <Link to="/login" className="nav-link">
                    ورود
                </Link>
            </li>
        </ul>
    );


    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <a className="navbar-brand mr-0 ml-5" href="#">
                یادگیری چرخه ی ماشین
            </a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>

            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav  text-right">
                    <li className="nav-item active">
                        <Link to="/selectProject" className="nav-link">
                            ساخت مدل یادگیری <span className="sr-only">(current)</span>
                        </Link>

                    </li>
                    
                    <li className="nav-item active">
                        <Link to="/webExtraction" className="nav-link">
                            استخراج داده های وب <span className="sr-only">(current)</span>
                        </Link>

                    </li>
                </ul>

                {isAuthenticated ? authLinks : guestLinks}
            </div>
        </nav>
    )
}

export default Header