import React, { Component, Fragment, useContext } from "react";
import ReactDom from "react-dom";
import Header from "./layout/Header";
import {
  HashRouter as Router,
  Route,
  Switch,
  Redirect,
} from "react-router-dom";
import Homepage from "./homePage/HomePage";
import Register from "./accounts/Register";
import Flow from "./flow/Flow";
import PrivateRoute from "./common/PrivateRoute";
import { Context } from "../Store";
import { loadUser } from "./actions/ActionAuth";

import Store from "../Store";
import Login from "./accounts/Login";
import SelectProject from "./selectProject/SelectProject";
import WebExtraction from "./webExtraction/WebExtraction";

const App = () => {
  const [state, dispatch] = useContext(Context);

  const isAuthenticated = state.auth.isAuthenticated;
  if (!isAuthenticated) {
    if (localStorage.getItem("token")) {
      loadUser();
    }
  }

  return (
    <Router>
      <Header />
      <Switch>
        <Route exact path="/" component={Homepage} />
        <PrivateRoute
          exact
          path="/register"
          callback="/"
          component={Register}
          authed={!state.auth.isAuthenticated}
        />
        <PrivateRoute
          exact
          path="/login"
          callback="/"
          component={Login}
          authed={!state.auth.isAuthenticated}
        />
        <PrivateRoute
          exact
          path="/selectProject"
          callback="/login"
          component={SelectProject}
          authed={state.auth.isAuthenticated}
        />
        <PrivateRoute
          exact
          path="/flow/:id"
          callback="/login"
          component={Flow}
          authed={state.auth.isAuthenticated}
        />
        <PrivateRoute
          exact
          path="/webExtraction"
          callback="/login"
          component={WebExtraction}
          authed={state.auth.isAuthenticated}
        />
      </Switch>
    </Router>
  );
};

ReactDom.render(
  <Store>
    <App />
  </Store>,
  document.getElementById("app")
);
