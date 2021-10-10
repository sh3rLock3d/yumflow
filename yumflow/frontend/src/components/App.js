import React, { Component, Fragment } from 'react';
import ReactDom from 'react-dom';
import Header from './layout/Header';
import Flows from './flows/Flows';
class App extends Component {
    render() {
        return (
            <>
            <Header />
            <Flows/>
            </>
        )
    }
}



ReactDom.render(<App />, document.getElementById('app'));