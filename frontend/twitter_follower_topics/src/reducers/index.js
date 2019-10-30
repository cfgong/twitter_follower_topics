import { combineReducers } from 'redux';
import dataReducer from './data';

const rootReducer = combineReducers({
  dataState: dataReducer
  
});

export default rootReducer;