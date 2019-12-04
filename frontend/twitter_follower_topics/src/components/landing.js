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
    this.handleClick = this.handleClick.bind(this);
  }

  handleChange(event){
    this.setState({search: event.target.value})
  }

  handleSubmit(event){
    event.preventDefault();
    store.dispatch({ type: 'LOADING_SET', payload: true})
    get_data(this.state.search);
    store.dispatch({ type: 'SEARCHED_SET', payload: this.state.search})
    const { history } = this.props;
    history.push("/results");
  }

  handleClick(event) {
    event.preventDefault();
    store.dispatch({ type: 'LOADING_SET', payload: true})
    get_data(event.target.getAttribute('name'));
    store.dispatch({ type: 'SEARCHED_SET', payload: event.target.getAttribute('name')})
    const { history } = this.props;
    history.push("/results");
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
              <td><a name="ewarren"  onClick={this.handleClick}>ewarren</a></td>
              <td><a name="realDonaldTrump" onClick={this.handleClick}>realDonaldTrump</a></td>
            </tr>
            <tr>
              <td><a name="JoeBiden" onClick={this.handleClick}>JoeBiden</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a name="SenSanders" onClick={this.handleClick}>SenSanders</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a name="KamalaHarris" onClick={this.handleClick}>KamalaHarris</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a name="CoryBooker" onClick={this.handleClick}>CoryBooker</a></td>
              <td></td>
            </tr>
            <tr>
              <td><a name="AndrewYang" onClick={this.handleClick}>AndrewYang</a></td>
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