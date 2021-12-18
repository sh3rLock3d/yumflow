import React from "react";
import { Route, Redirect } from "react-router-dom";

const PrivateRoute = ({ component: Component, authed, callback, ...rest }) => {
  return (
    <Route
      {...rest}
      render={(props) =>
        authed ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{ pathname: callback, state: { from: props.location } }}
          />
        )
      }
    />
  );
};

export default PrivateRoute;
