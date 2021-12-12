import React, { useEffect, useContext, useState } from "react";
import { Link, Redirect } from "react-router-dom";
import { Context } from "../../Store";
import { register } from "../actions/ActionAuth";
import { REGISTER_SUCCESS } from "../actions/types";
import { useHistory } from "react-router-dom";
import Snackbar from "../common/MySnackbar";
import TextField from "../common/MyTextField";

const Register = () => {
  const [state, dispatch] = useContext(Context);
  const [error, setError] = useState("");
  const [passwordsDontMatch, setPasswordsDontMatch] = useState("");
  const history = useHistory();

  const onSubmit = (e) => {
    console.log("hello");
    e.preventDefault();
    let username = document.getElementById("formRegisterusername").value;
    let email = document.getElementById("formRegisterEmail").value;
    let password = document.getElementById("formRegisterpass1").value;
    let password2 = document.getElementById("formRegisterpass2").value;
    if (password !== password2) {
      console.log("error Passwords do not match");
      setPasswordsDontMatch("رمز عبور یکسان نیست!");
    } else {
      const newUser = {
        username,
        password,
        email,
      };
      register(newUser)
        .then((data) => data.json())
        .then((data) => {
          console.log("success", data);
          if (data.username) throw new Error(data.username[0]);
          dispatch({ type: REGISTER_SUCCESS, payload: data });
          history.push("/");
        })
        .catch((error) => {
          setError(error.message);
        });
    }
  };

  return (
    <div className="col-md-6 m-auto">
      <div className="card card-body mt-5 my-card">
        <h2 className="text-center">ثبت نام</h2>
        <form onSubmit={onSubmit}>
          <div className="text-center m-2">
            <TextField id="formRegisterusername" label="نام کاربری" />
          </div>

          <div className="text-center m-2">
            <TextField
              id="formRegisterEmail"
              label="پست الکترونیک"
              type="email"
              dir="ltr"
            />
          </div>

          <div className="text-center m-2">
            <TextField
              id="formRegisterpass1"
              label="رمز عبور"
              type="password"
            />
          </div>

          <div className="text-center m-2">
            <TextField
              id="formRegisterpass2"
              label="تکرار رمز عبور"
              type="password"
            />
          </div>

          <div className="form-group text-center">
            <button type="submit" className="btn btn-primary">
              ثبت نام
            </button>
          </div>
          <p className="text-center">
            حساب کاربری دارید؟ <Link to="/login">ورود</Link>
          </p>
        </form>
      </div>

      <Snackbar
        open={!!error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
      <Snackbar
        open={!!passwordsDontMatch}
        onClose={() => setPasswordsDontMatch("")}
        message={passwordsDontMatch}
        variant="error"
      />
    </div>
  );
};

export default Register;
