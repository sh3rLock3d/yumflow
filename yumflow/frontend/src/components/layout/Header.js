import React, {useEffect, useContext} from 'react';
import { Link } from 'react-router-dom';
import {Context} from '../../Store'

function Header() {
    const [state, dispatch] = useContext(Context);
    
    const isAuthenticated = state.auth.isAuthenticated
    const user  =  state.auth.user


    
    const authLinks = (
        <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
            <span className="navbar-text ml-3">
                <strong>{user ? `Welcome ${user.username}` : ''}</strong>
            </span>
            <li className="nav-item">
                <button className="nav-link btn btn-info btn-sm text-light">
                    Logout
                </button>
            </li>
        </ul>
    );
    
    

    const guestLinks = (
        <ul className="navbar-nav ml-auto mt-2 mt-lg-0">
            <li className="nav-item">
                <Link to="/register" className="nav-link">
                    Register
                </Link>
            </li>
            <li className="nav-item">
                <Link to="/login" className="nav-link">
                    Login
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
                        <a className="nav-link" href="#"> استخراج داده های وب </a>
                    </li>

                    <li className="nav-item active">
                        <a className="nav-link" href="#"> ثبت نام </a>
                    </li>

                </ul>

                {isAuthenticated ? authLinks : guestLinks}
            </div>
        </nav>
    )
}

export default Header