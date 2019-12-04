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
  }

  render() {

    console.log(this.props.chart_data)

    return (
    	<div>
        <VictoryChart
          width={275} height={175}
          domainPadding={20}
          theme={VictoryTheme.material}
          //animate={{ duration: 100}}
          >
          <VictoryAxis
          label = {this.props.word_type}
          // tickValues specifies both the number of ticks and where
          // they are placed on the axis
          tickFormat={this.props.labels}
          style={(this.props.word_type != "hashtag") ? ({
            axisLabel: {fontSize: 5, padding:20},
            tickLabels: {fontSize: 3, angle:45}
          }) : ({
                          axisLabel: {fontSize: 5, padding:27},
                          tickLabels: {fontSize: 3, angle:45}
                        })}
        />
        <VictoryAxis
          label = {this.props.word_type + " count"}
          dependentAxis
          style={{
            axisLabel: {fontSize: 5, padding:30},
            tickLabels: {fontSize: 5}
          }}
        />
          <VictoryBar
            labels = {this.props.counts}
          animate={{
            onLoad: { duration: 600 }
          }}
            data = {this.props.chart_data}
            x = {this.props.word_type}
            y = {this.props.word_type + "_count"}
            style={{ labels: { fontSize: 4, padding: 1 } }}
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

