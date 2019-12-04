import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { 
  get_data, } from '../functions';
import '../style/landing.css';

import { connect } from 'react-redux'
import { compose } from 'redux';
import store from '../store';


class LandingPage extends Component {

  constructor(props){
    super(props);
    this.state = {search: ''}
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event){
    this.setState({search: event.target.value})
  }

  handleSubmit(event){
    event.preventDefault();
    get_data(this.state.search);
    store.dispatch({ type: 'SEARCHED_SET', payload: this.state.search})
    const { history } = this.props;
    history.push("/results");
  }

  handleClick(parameter) {
    console.log(parameter);
    // get_data(parameter);
    // const { history } = this.props;
    // history.push("/results");
    // console.log("2");
  }


  render() {
    return (
        <>
        <div>
        <h1>TopicTracker</h1>
        <p>Welcome! TopicTracker is a tool to determine key topics that supporters of political candidates are interested in and care about. Enter a political candidate's Twitter handle below (without the @). The output is two histograms with the most relevant topics followers of that candidate care about. Try it out!</p>
        <form onSubmit={this.handleSubmit}>
          <input type="text" value={this.state.search} className="searchbar" placeholder="Enter a Twitter Handle" onChange={this.handleChange} />
          <input type="submit" value="Submit" />
        </form>
        </div>
        <h3>Candidate Suggestions (cached)</h3>
        <table>
          <thead>
            <tr>
              <th>Democrat</th>
              <th>Republican</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('ewarren')}>ewarren</a></td>
              <td><a href="results.js" onClick={this.handleClick('realDonaldTrump')}>realDonaldTrump</a></td>
            </tr>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('JoeBiden')}>JoeBiden</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('SenSanders')}>SenSanders</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('KamalaHarris')}>KamalaHarris</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('CoryBooker')}>CoryBooker</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a href="results.js" onClick={this.handleClick('AndrewYang')}>AndrewYang</a></td>
              <td></td>
            </tr>
          </tbody>
          </table>
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
)(LandingPage);