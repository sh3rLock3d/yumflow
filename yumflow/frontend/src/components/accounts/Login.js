import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { Context } from "../../Store";
import { login } from "../actions/ActionAuth";
import { LOGIN_SUCCESS } from "../actions/types";
import { useHistory } from "react-router-dom";
import Snackbar from "../common/MySnackbar";
import TextField from "../common/MyTextField";

function Login() {
  /*
    const state = {
        username: '',
        password: '',
    };
    */
  const [state, dispatch] = useContext(Context);
  const [error, setError] = useState("");

  const history = useHistory();

  const onSubmit = (e) => {
    e.preventDefault();
    //this.props.login(this.state.username, this.state.password);
    let username = document.getElementById("LoginUsernameInput").value;
    let password = document.getElementById("LoginPasswordInput").value;

    login(username, password)
      .then((data) => data.json())
      .then((data) => {
        console.log("success", data);
        if (data.non_field_errors) throw new Error(data.non_field_errors[0]);
        dispatch({ type: LOGIN_SUCCESS, payload: data });
        history.push("/");
      })
      .catch((error) => {
        console.log(error);
        setError(error.message);
      });
  };

  return (
    <div className="col-md-6 m-auto">
      <div className="card card-body mt-5 my-card">
        <h2 className="text-center">ورود</h2>
        <form onSubmit={onSubmit}>
          <div className="text-center m-2s">
            <TextField id="LoginUsernameInput" label="نام کاربری" />
          </div>

          <div className="text-center m-2">
            <TextField
              id="LoginPasswordInput"
              label="رمز عبور"
              type="password"
            />
          </div>

          <div className="form-group text-center">
            <button type="submit" className="btn btn-primary">
              ورود
            </button>
          </div>
          <p className="text-center">
            حساب کاربری ندارید؟ <Link to="/register">ثبت نام</Link>
          </p>
        </form>
      </div>
      <Snackbar
        open={!!error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
    </div>
  );
}

export default Login;
