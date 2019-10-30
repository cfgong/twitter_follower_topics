import store from '../store';

const axios = require('axios');

export function get_data(str){
    const params = new URLSearchParams();
    params.append('twitter_handle', str);
    axios({
      method: 'POST',
      url: 'http://127.0.0.1:5000/predict',
      data: params
    })
    .then(function (response) {
      console.log("GOT RESPONSE FROM SERVER");
      store.dispatch({ type: 'DATA_SET', payload: response["data"]["data"]})

    })
    .catch(function (error) {
      console.log(error);
    });
  }