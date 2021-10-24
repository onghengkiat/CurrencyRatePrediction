import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Navbar from '../Navbar/Navbar';
import Home from '../Home/Home';
import Dashboard from '../Dashboard/Dashboard';
import Spinner from '../Spinner/Spinner';

import useError from '../../hooks/useError';
import useSuccess from '../../hooks/useSuccess';
import useLoading from '../../hooks/useLoading';

import ErrorToast from '../Toast/ErrorToast';
import SuccessToast from '../Toast/SuccessToast';

function App() {
  const { error, setError } = useError();
  const { success, setSuccess } = useSuccess();
  const { loading, setLoading } = useLoading();

  return (
      <BrowserRouter>
        <ErrorToast error={ error } setError={ setError }/>
        <SuccessToast success={ success } setSuccess={ setSuccess }/>
        <Spinner loading={ loading } />
        <Switch>

          <Route path="/dashboard">
            <Navbar/>      
            <Dashboard setError={ setError } setLoading={ setLoading } loading= {loading}/>
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