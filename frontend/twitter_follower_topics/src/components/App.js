import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';
import * as routes from '../constants/routes';

import LandingPage from './landing';
import ResultsPage from './results';
import BarChart from './barchart';

const App = () =>
  <Router>
    <Switch>
      <Route exact path={routes.LANDING} component={() => <LandingPage />} />
      <Route path={routes.RESULTS} component={() => <ResultsPage />} />
    </Switch>
  </Router>

export default App;