const URL = "http://127.0.0.1:8000/api/";
import { USER_LOADED, LOGOUT_SUCCESS } from "../actions/types";
import { Context } from "../../Store";
import React, { useEffect, useContext } from "react";

// LOGIN USER
export const login = (username, password) => {
  // Request Body
  const data = { username, password };

  let link = URL + "auth/login";
  return fetch(link, {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
};

export const register = (data) => {
  let link = URL + "auth/register";
  return fetch(link, {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
};

export const loadUser = (history, redirect) => {
  // User Loading
  //dispatch({ type: USER_LOADING });
  const [state, dispatch] = useContext(Context);

  fetch("/api/auth/user", tokenConfig())
    .then((response) => response.json())
    .then((res) => {
      if (res["detail"]) {
        throw new Error("error");
      }
      dispatch({ type: USER_LOADED, payload: res });
      history.replace(redirect);
    })
    .catch((err) => {
      console.log(err);
      console.log("token not valid");
      //todo       dispatch({type: AUTH_ERROR,});
      localStorage.removeItem("token");
    });
};

export const logout = (dispatch) => {
  return new Promise((resolve, reject) => {
    let link = "/api/auth/logout/";
    fetch(link, {
      method: "POST",
      headers: tokenConfig().headers,
    })
      .then((data) => {
        if (200 <= data.status < 300) {
          dispatch({ type: LOGOUT_SUCCESS, payload: data });
          resolve();
        } else {
          throw new Error("error");
        }
      })
      .catch((err) => {
        console.log(err);
        reject();
      });
  });
};

// Setup config with token - helper function
export const tokenConfig = () => {
  // Get token from state
  const token = localStorage.getItem("token");

  // Headers
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // If token, add to headers config
  if (token) {
    config.headers["Authorization"] = `Token ${token}`;
  }

  return config;
};

export const tokenConfigForm = () => {
  // Get token from state
  const token = localStorage.getItem("token");

  // Headers
  const config = {
    headers: {},
  };

  // If token, add to headers config
  if (token) {
    config.headers["Authorization"] = `Token ${token}`;
  }

  return config;
};
