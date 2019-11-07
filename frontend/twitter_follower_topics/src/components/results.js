import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import { compose } from 'redux';
import * as d3 from "d3";
import * as routes from '../constants/routes';
import { 
  isEmpty, } from '../functions';

import BarChart from './barchart';

class ResultsPage extends Component {

  constructor(props){
    super(props);
  }

  render() {

    return (
      <div>
      <Link to={routes.LANDING}>Back to home page</Link>
      <BarChart />
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
