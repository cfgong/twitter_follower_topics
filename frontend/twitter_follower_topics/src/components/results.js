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
import Loader from 'react-loader-spinner'

class ResultsPage extends Component {

  constructor(props){
    super(props);
  }

  render() {

    var token_data = [];
    var hashtag_data = [];

    if(!isEmpty(this.props.data)){

      

      for(var i = 0; i < this.props.data.hash_counts.length; i++){

        hashtag_data.push({hashtag:this.props.data.hash_labels[i], hashtag_count:this.props.data.hash_counts[i]})
      }

      for(var i = 0; i < this.props.data.token_counts.length; i++){

        token_data.push({word:this.props.data.token_labels[i], word_count:this.props.data.token_counts[i]})
      }

    }

    console.log(this.props.loading);

    let content = (this.props.loading) ? (<Loader
         type="Circles"
         color="brown"
         height={100}
         width={100}
         class = "loader"
         timeout={99999999} //3 secs

      />) : (<><BarChart chart_data = {token_data} counts={this.props.data.token_counts} labels={this.props.data.token_labels} word_type = "word" className="chart"/>
        <BarChart chart_data = {hashtag_data} counts={this.props.data.hash_counts} labels={this.props.data.hash_labels} word_type = "hashtag" className="chart"/></>)

    return (
      <div>
      <h1>TopicTracker</h1>
      <p><Link to={routes.LANDING}>Back to home page</Link></p>
      <p>Below are two histrograms with 15 of the most used hashtags and words (topics) for followers of @{this.props.searched}</p>


      <div className="chartSpace">
        {content}
      </div>

      
      </div>
      );
  }
}

const mapStateToProps = (state) => ({
  data: state.dataState.data,
  searched: state.searchedState.searched,
  loading: state.loadingState.loading,

});

export default compose(
  withRouter,
  connect(mapStateToProps),
)(ResultsPage);
