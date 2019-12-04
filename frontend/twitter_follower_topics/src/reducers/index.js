import { combineReducers } from 'redux';
import dataReducer from './data';
import searchedReducer from './searched';
import loadingReducer from './loading';

const rootReducer = combineReducers({
  dataState: dataReducer,
  searchedState: searchedReducer,
  loadingState: loadingReducer,
  
});

export default rootReducer;