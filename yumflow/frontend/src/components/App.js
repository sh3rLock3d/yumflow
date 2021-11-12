import React, { Component, Fragment, useContext } from 'react';
import ReactDom from 'react-dom';
import Header from './layout/Header';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Homepage from './homePage/HomePage';
import Register from './accounts/Register';
import Flow from './flow/Flow'
import PrivateRoute from './common/PrivateRoute';
import { Context } from '../Store';

import Store from '../Store';
import Login from './accounts/Login';
import SelectProject from './selectProject/SelectProject';
import WebExtraction from './webExtraction/WebExtraction';

const App = () => {
    const [state, dispatch] = useContext(Context);
    
    return (
            <Router>
                <Header />
                <Switch>
                    <Route exact path="/" component={Homepage} />
                    <PrivateRoute exact path="/register" component={Register} authed={!state.auth.isAuthenticated} />
                    <PrivateRoute exact path="/login" component={Login} authed={!state.auth.isAuthenticated} />
                    <PrivateRoute exact path="/selectProject" component={SelectProject} authed={state.auth.isAuthenticated} />
                    <PrivateRoute exact path="/flow/:id" component={Flow} authed={state.auth.isAuthenticated} />
                    <PrivateRoute exact path="/webExtraction" component={WebExtraction} authed={state.auth.isAuthenticated} />
                </Switch>
            </Router>
    )
}

ReactDom.render((<Store><App /></Store>), document.getElementById('app'));