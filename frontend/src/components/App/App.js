import React, { useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

import Navbar from '../Navbar/Navbar';
import Home from '../Home/Home';
import Dataset from '../Dataset/Dataset';
import Spinner from '../Spinner/Spinner';
import Statistics from '../Statistics/Statistics';
import Dashboard from '../Dashboard/Dashboard';
import Login from '../Login/Login';
import Logout from '../Logout/Logout';
import UserList from '../UserAccount/UserList';
import UserProfile from '../UserAccount/UserProfile';
import ChangePassword from '../UserAccount/ChangePassword';

import AuthRoute from '../AuthRoute/AuthRoute';

import useError from '../../hooks/useError';
import useSuccess from '../../hooks/useSuccess';
import useLoading from '../../hooks/useLoading';
import useToken from '../../hooks/useToken';

import ErrorToast from '../Toast/ErrorToast';
import SuccessToast from '../Toast/SuccessToast';

function App() {
  const { token, setToken } = useToken();
  const { error, setError } = useError();
  const { success, setSuccess } = useSuccess();
  const { loading, setLoading } = useLoading();

  return (
      <BrowserRouter>
        <ErrorToast error={ error } setError={ setError }/>
        <SuccessToast success={ success } setSuccess={ setSuccess }/>
        <Spinner loading={ loading } />
        <Navbar token={ token }/>

        <Switch>

          <AuthRoute path="/dataset" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}>
            <Dataset setError={ setError } setLoading={ setLoading }/>
          </AuthRoute>

          <AuthRoute path="/statistic" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}>
            <Statistics token={ token } setError={ setError } setLoading={ setLoading }/>
          </AuthRoute>

          <AuthRoute path="/dashboard" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}>
            <Dashboard token={ token } setError={ setError } setLoading={ setLoading }/>
          </AuthRoute>

          <AuthRoute path="/login" type="GUEST" token={ token }>
            <Login setToken={ setToken } setError={ setError }/>
          </AuthRoute>

          <AuthRoute path="/logout" type="GUEST" token={ token }>
            <Logout token={ token } setToken={ setToken }/>
          </AuthRoute>

          <AuthRoute path="/user" type="PRIVATE" token={ token } rolesAllowed={["admin"]}>
            <UserList setError={ setError } token={ token } setSuccess={ setSuccess }/>
          </AuthRoute>

          <AuthRoute path="/profile/view" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}>
            <UserProfile setError={ setError } token={ token } editing={ false }/>
          </AuthRoute>

          <AuthRoute path="/profile/edit" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}> 
            <UserProfile setError={ setError } token={ token } editing={ true } setSuccess={ setSuccess } setToken={ setToken }/>
          </AuthRoute>

          <AuthRoute path="/password" type="PRIVATE" token={ token } rolesAllowed={["admin", "developer", "viewer"]}>    
            <ChangePassword setError={ setError } setSuccess={ setSuccess } token={ token }/>
          </AuthRoute>

          <Route path="/">
            <Home setError={ setError }/>
          </Route>
          
        </Switch>
      </BrowserRouter>
  );
}

export default App;