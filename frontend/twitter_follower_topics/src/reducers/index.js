import { combineReducers } from 'redux';
import dataReducer from './data';
import searchedReducer from './searched';

const rootReducer = combineReducers({
  dataState: dataReducer,
  searchedState: searchedReducer,
  
});

export default rootReducer;