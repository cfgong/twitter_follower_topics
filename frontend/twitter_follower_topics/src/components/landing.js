import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router, withRouter } from 'react-router-dom'
import { 
  get_data, } from '../functions';

import { connect } from 'react-redux'
import { compose } from 'redux';


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
    const { history } = this.props;
    history.push("/results");
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input type="text" value={this.state.search} className="searchbar" placeholder="Search" onChange={this.handleChange} />
        <input type="submit" value="Submit" />
      </form>
      );
  }
}


const mapStateToProps = (state) => ({
    data: state.dataState.data,

  });

export default compose(
  withRouter,
  connect(mapStateToProps),
)(LandingPage);