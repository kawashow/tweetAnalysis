import React, { Component } from "react";
import { render } from "react-dom";
import ReactDOM from "react-dom";

console.log("djando restart test!");
class Layout extends React.Component {
    render() {
      return (
        <h1>Welcome!</h1>
      );
    }
  }

  const app = document.getElementById('app');
  ReactDOM.render(<Layout/>, app);