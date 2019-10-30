import React from 'react';
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';
import * as routes from '../constants/routes';

import LandingPage from './landing';
import ResultsPage from './results';

const App = () =>
  <Router>
    <div>
      <Route exact path={routes.LANDING} component={() => <LandingPage />} />
      <Route exact path={routes.RESULTS} component={() => <ResultsPage />} />
    </div>
  </Router>

export default App;