import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import './index.css';

const axios = require('axios');

class LandingPage extends Component {

  constructor(props){
    super(props);
    this.state = {search: ''}
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(str){
    const params = new URLSearchParams();
    params.append('twitter_handle', str);
    axios({
      method: 'POST',
      url: 'http://127.0.0.1:5000/predict',
      data: params
    })
    .then(function (response) {
      console.log(response);

      console.log(response["statusText"])
      this.props.history.push('/searchresults')
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  handleChange(event){
    this.setState({search: event.target.value})
  }

  handleSubmit(event){
    event.preventDefault();
    this.handleSearch(this.state.search)
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

// ========================================

ReactDOM.render(
  <LandingPage />,
  document.getElementById('root')
);

