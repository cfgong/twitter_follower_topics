import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import { compose } from 'redux';
import * as d3 from "d3";
import * as routes from '../constants/routes';
import { 
  isEmpty, } from '../functions';

class BarChart extends Component {
componentDidUpdate() {
this.drawChart();
}

drawChart() {

	if(!isEmpty(this.props.data)){
      const data = this.props.data["counts"];
      const count = this.props.data["counts"];
      const labels = this.props.data["labels"];
      console.log("DATA FOR BAR CHART: ", labels);
const svg = d3.select("body").append("svg")
  .attr("width", this.props.width)
  .attr("height", this.props.height);

const h = this.props.height;

svg.selectAll("rect")
.data(data)
.enter()
.append("rect")
.attr("x", (d, i) => i * 70)
.attr("y", (d, i) => h - 10 * d)
.attr("width", 25)
.attr("height", (d, i) => d * 10)
.attr("fill", "green");

svg.selectAll("text")
.data(data)
.enter()
.append("text")
.text((d) => d)
.attr("x", (d, i) => i * 70)
.attr("y", (d, i) => h - (10 * d) - 3)

    }


}

render() {
return (

	<div>
	<svg></svg>
	</div>
	)
}

}

const mapStateToProps = (state) => ({
  data: state.dataState.data,

});

export default connect(mapStateToProps)(BarChart)

