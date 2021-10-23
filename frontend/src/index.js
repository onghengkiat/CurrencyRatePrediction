import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App/App';
import 'bootstrap/dist/css/bootstrap.min.css';

import ErrorBoundary from './components/ErrorHandler/ErrorBoundary';

ReactDOM.render(
  <ErrorBoundary>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </ErrorBoundary>,
  document.getElementById('root')
);

