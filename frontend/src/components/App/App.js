import React, { useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Navbar from '../Navbar/Navbar';
import Home from '../Home/Home';
import Dataset from '../Dataset/Dataset';
import Spinner from '../Spinner/Spinner';
import Statistics from '../Statistics/Statistics';
// import Dashboard from '../Dashboard/Dashboard';

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
        <Switch>

          <Route path="/dataset">
            <Navbar/>      
            <Dataset setError={ setError } setLoading={ setLoading }/>
          </Route>

          <Route path="/statistic">
            <Navbar/>      
            <Statistics setError={ setError } setLoading={ setLoading }/>
          </Route>

          {/* <Route path="/dashboard">
            <Navbar/>      
            <Dashboard setError={ setError } setLoading={ setLoading }/>
          </Route> */}

          <Route path="/">
            <Navbar/>      
            <Home setError={ setError }/>
          </Route>
          
        </Switch>
      </BrowserRouter>
  );
}

export default App;