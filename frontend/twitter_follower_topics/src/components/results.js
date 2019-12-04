import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import { compose } from 'redux';
import * as d3 from "d3";
import * as routes from '../constants/routes';
import { 
  isEmpty, } from '../functions';

import '../style/landing.css';

import BarChart from './barchart';

class ResultsPage extends Component {

  constructor(props){
    super(props);
  }

  render() {

    return (
      <>
      <h1>TopicTracker</h1>
      <p>Below are two histrograms with 15 of the most used hashtags and words (topics) for followers of @{this.props.searched}</p>

      

      <div className="chartSpace">
        <BarChart counts={this.props.data["hash_counts"]} labels={this.props.data["hash_labels"]} className="chart"/>
        <BarChart counts={this.props.data["token_counts"]} labels={this.props.data["token_labels"]} className="chart"/>
      </div>

      <p><Link to={routes.LANDING}>Back to home page</Link></p>
      </>
      );
  }
}

const mapStateToProps = (state) => ({
  data: state.dataState.data,
  searched: state.searchedState.searched
});

export default compose(
  withRouter,
  connect(mapStateToProps),
)(ResultsPage);
