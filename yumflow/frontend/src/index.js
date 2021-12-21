import ReactDom from "react-dom";
import React from "react";
import Store from "./Store";
import { HashRouter as Router } from "react-router-dom";
import App from "./components/App";

ReactDom.render(
  <Store>
    <Router>
      <App />
    </Router>
  </Store>,
  document.getElementById("app")
);
