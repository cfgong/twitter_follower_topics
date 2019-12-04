import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import { compose } from 'redux';
import * as d3 from "d3";
import * as routes from '../constants/routes';
import { 
  isEmpty, } from '../functions';

import { VictoryBar, VictoryChart, VictoryAxis, VictoryTheme } from 'victory';

class BarChart extends Component {

  constructor(props){
    super(props);
    //this.drawChart = this.drawChart.bind(this);
  }

  render() {

    console.log("props",this.props.data);
    console.log("searched", this.props.searched)

    var token_data = [];
    var hashtag_data = [];

    if(!isEmpty(this.props.data)){

      

      for(var i = 0; i < this.props.data.hash_counts.length; i++){

        token_data.push({word:this.props.data.token_labels[i], word_count:this.props.data.token_counts[i]})
        hashtag_data.push({hashtag:this.props.data.hash_labels[i], hashtag_count:this.props.data.hash_counts[i]})
      }

    }

    //this.drawChart();

    return (
    	<div>
        <VictoryChart
          width={300} height={200}
          domainPadding={20}
          theme={VictoryTheme.material}
          >
          <VictoryAxis
          label = {"Word"}
          // tickValues specifies both the number of ticks and where
          // they are placed on the axis
          tickFormat={this.props.data.token_labels}
          style={{
            axisLabel: {fontSize: 7, padding:20},
            tickLabels: {fontSize: 3}
          }}
        />
        <VictoryAxis
          label = {"Word Count"}
          dependentAxis
          style={{
            axisLabel: {fontSize: 7, padding:30},
            tickLabels: {fontSize: 5}
          }}
        />
          <VictoryBar
            data = {token_data}
            x = "word"
            y = "word_count"
          />
        </VictoryChart>
      </div>
    	);
  }

}

const mapStateToProps = (state) => ({
  data: state.dataState.data,
  searched: state.searchedState.searched,

});

export default compose(
  withRouter,
  connect(mapStateToProps),
)(BarChart);

