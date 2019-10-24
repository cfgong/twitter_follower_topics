import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

const axios = require('axios');

function handleSearch(str){
  const params = new URLSearchParams();
  params.append('twitter_handle', str);
  axios({
    method: 'POST',
    url: 'http://127.0.0.1:5000/predict',
    data: params
})
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });
}

class LandingPage extends Component {

  constructor(props){
    super(props);
    this.state = {search: ''}
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
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  handleChange(event){
    this.setState({search: event.target.value})
  }

  handleSubmit(event){
    this.handleSearch(this.state.search)
  }

  render() {
    console.log(this.state.search)
    return (
      <form onSubmit={this.handleSubmit.bind(this)}>
        <input type="text" value={this.state.search} className="searchbar" placeholder="Search" onChange={this.handleChange.bind(this)} />
      </form>
      );
  }
}

class Square extends Component {
  render() {
    return (
      <button className="square">
        {/* TODO */}
      </button>
    );
  }
}

// ========================================

ReactDOM.render(
  <LandingPage />,
  document.getElementById('root')
);

