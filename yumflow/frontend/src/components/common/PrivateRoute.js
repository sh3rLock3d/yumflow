import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

const PrivateRoute = ({ component: Component, authed, ...rest }) => {
    return (
        <Route
            {...rest}
            render={(props) => authed ? <Component {...props} /> : <Redirect to={{pathname: '/login'}} />}
        />
    )
}

export default PrivateRoute;
