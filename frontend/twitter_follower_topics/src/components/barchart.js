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

  // drawChart() {

  // 	if(!isEmpty(this.props.data)){
  //       const count = this.props.counts;
  //       const labels = this.props.labels;

  //       var data = []
  //       for(var i = 0; i < count.length; i++){
  //         data.push({"word": labels[i], "freq": count[i]});
  //       }

  //       var margin = {top: 20, right: 20, bottom: 30, left: 40},
  //       width = 1200 - margin.left - margin.right,
  //       height = 500 - margin.top - margin.bottom;

  //       var svg = d3.select("body").append("svg")
  //       .attr("width", width + margin.left + margin.right)
  //       .attr("height", height + margin.top + margin.bottom)
  //       .append("g")
  //       .attr("transform", 
  //             "translate(" + margin.left + "," + margin.top + ")");

  //       var x = d3.scaleBand()
  //         .range([0, width])
  //         .padding(0.1);
  //       var y = d3.scaleLinear()
  //         .range([height, 0]);


  //       x.domain(data.map(function(d) { return d.word; }));
  //       y.domain([0, d3.max(data, function(d) { return d.freq; })]);

  //       svg.selectAll(".bar")
  //       .data(data)
  //       .enter()
  //       .append("rect")
  //       .attr("class", "bar")
  //       .attr("x", function(d) { return x(d.word); })
  //       .attr("width", x.bandwidth())
  //       .attr("y", function(d) { return y(d.freq); })
  //       .attr("height", function(d) { return height - y(d.freq); });

  //       svg.append("g")
  //       .attr("transform", "translate(0," + height + ")")
  //       .call(d3.axisBottom(x));

  //       svg.append("g")
  //       .call(d3.axisLeft(y));
  //   }
  // }

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

