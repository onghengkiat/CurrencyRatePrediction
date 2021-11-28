import React, { useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

import Navbar from '../Navbar/Navbar';
import Home from '../Home/Home';
import Dataset from '../Dataset/Dataset';
import Spinner from '../Spinner/Spinner';
import Statistics from '../Statistics/Statistics';
import Dashboard from '../Dashboard/Dashboard';

import useError from '../../hooks/useError';
import useSuccess from '../../hooks/useSuccess';
import useLoading from '../../hooks/useLoading';

import ErrorToast from '../Toast/ErrorToast';
import SuccessToast from '../Toast/SuccessToast';

function App() {
  const { error, setError } = useError();
  const { success, setSuccess } = useSuccess();
  const { loading, setLoading } = useLoading();

  useEffect(() => {
    document.title = "CurEx"
  }, [])

  return (
      <BrowserRouter>
        <ErrorToast error={ error } setError={ setError }/>
        <SuccessToast success={ success } setSuccess={ setSuccess }/>
        <Spinner loading={ loading } />
        <Navbar/>

        <Switch>

          <Route path="/dataset">
            <Dataset setError={ setError } setLoading={ setLoading }/>
          </Route>

          <Route path="/statistic">
            <Statistics setError={ setError } setLoading={ setLoading }/>
          </Route>

          <Route path="/dashboard">
            <Dashboard setError={ setError } setLoading={ setLoading }/>
          </Route>

          <Route path="/">
            <Home setError={ setError }/>
          </Route>
          
        </Switch>
      </BrowserRouter>
  );
}

export default App;