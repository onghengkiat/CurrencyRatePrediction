import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Navbar from '../Navbar/Navbar';
import Home from '../Home/Home';
import Dashboard from '../Dashboard/Dashboard';

import useError from '../../hooks/useError';
import useSuccess from '../../hooks/useSuccess';

import ErrorToast from '../Toast/ErrorToast';
import SuccessToast from '../Toast/SuccessToast';

function App() {
  const { error, setError } = useError();
  const { success, setSuccess } = useSuccess();
  
  return (
      <BrowserRouter>
        <ErrorToast error={ error } setError={ setError }/>
        <SuccessToast success={ success } setSuccess={ setSuccess }/>
        <Switch>

          <Route path="/dashboard">
            <Navbar/>      
            <Dashboard setError={ setError }/>
          </Route>

          <Route path="/model">
            <Navbar/>      
            <Home setError={ setError }/>
          </Route>

          <Route path="/">
            <Navbar/>      
            <Home setError={ setError }/>
          </Route>
          
        </Switch>
      </BrowserRouter>
  );
}

export default App;