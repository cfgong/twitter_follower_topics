import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import { compose } from 'redux';
import * as d3 from "d3";
import * as routes from '../constants/routes';
import { 
  isEmpty, } from '../functions';

class ResultsPage extends Component {

  constructor(props){
    super(props);
  }

  render() {

    if(!isEmpty(this.props.data)){
      console.log("PROPS GOT DATA");
      console.log(this.props.data);

    }

    return (
      <div>
      RESULTSPAGE
      <Link to={routes.LANDING}>Back to home page</Link>
      </div>
      );
  }
}

const mapStateToProps = (state) => ({
  data: state.dataState.data,

});

export default compose(
  withRouter,
  connect(mapStateToProps),
)(ResultsPage);
