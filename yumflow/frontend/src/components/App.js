import React, { Component, Fragment } from 'react';
import ReactDom from 'react-dom';
import Header from './layout/Header';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Homepage from './homePage/HomePage';
import Register from './accounts/Register';
import Flow from './flow/Flow'


import Store from '../Store';
import Login from './accounts/Login';
import SelectProject from './selectProject/SelectProject';

class App extends Component {
    render() {
        return (
            <Store>
                <Router>
                    <Header />
                    <Switch>

                        <Route exact path="/" component={Homepage} />
                        <Route exact path="/register" component={Register} />
                        <Route exact path="/login" component={Login} />
                        <Route exact path="/selectProject" component={SelectProject} />
                        <Route exact path="/flow/:id" component={Flow} />
                    </Switch>
                </Router>
            </Store>
        )
    }
}



ReactDom.render(<App />, document.getElementById('app'));