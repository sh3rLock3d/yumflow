import React, { useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../../Store";
import { logout } from "../actions/ActionAuth";
import { useHistory } from "react-router-dom";

function Header() {
  const [state, dispatch] = useContext(Context);
  const history = useHistory();
  const isAuthenticated = state.auth.isAuthenticated;
  const user = state.auth.user;

  const logoutUser = () => {
    logout(dispatch)
      .then(() => {
        history.push("/");
      })
      .catch(() => {});
  };

  const authLinks = (
    <ul className="navbar-nav me-auto mt-2 mt-lg-0">
      <li className="nav-item" style={{ padding: "0.5rem" }}>
        <span>
          <strong>{user ? `کاربر فعلی: ${user.username}` : ""}</strong>
        </span>
      </li>
      <li className="nav-item active">
        <button
          className="nav-link btn btn-link btn-sm"
          style={{ margin: "auto", color: "tomato" }}
          onClick={logoutUser}
        >
          خروج
        </button>
      </li>
    </ul>
  );

  const guestLinks = (
    <ul className="navbar-nav me-auto mt-2 mt-lg-0">
      <li className="nav-item">
        <Link to="/register" className="btn btn-primary">
          ثبت نام
        </Link>
      </li>
      <li className="nav-item">
        <Link to="/login" className="btn btn-primary">
          ورود
        </Link>
      </li>
    </ul>
  );

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <a className="navbar-brand me-3 ms-5" href="#">
        یادگیری چرخه ی ماشین
      </a>
      <button
        className="navbar-toggler ms-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div
        className="collapse navbar-collapse ms-3"
        id="navbarSupportedContent"
      >
        {isAuthenticated && (
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/selectProject" className="btn btn-primary">
                ساخت مدل یادگیری
              </Link>
            </li>

            <li className="nav-item">
              <Link to="/webExtraction" className="btn btn-primary">
                استخراج داده‌های وب
              </Link>
            </li>
          </ul>
        )}
        <hr />

        {isAuthenticated ? authLinks : guestLinks}
      </div>
    </nav>
  );
}

export default Header;
