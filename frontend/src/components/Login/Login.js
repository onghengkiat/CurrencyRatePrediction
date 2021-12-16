import React, { useState } from 'react';
import { URL_PREFIX } from '../../constants/API';
import PropTypes from 'prop-types';
import './Login.css';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { BACKEND_SERVER_ERROR } from '../../constants/error';

/////////////////// 
//   API Calls   //
///////////////////

async function loginUser(credentials) {
  return fetch(`${URL_PREFIX}authenticate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }

    throw response;
  })
  .then(data => data)
  .catch(response => { 
    // case when backend server is working, and sent frontend the error message
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}



///////////////////// 
//   HTML Object   //
/////////////////////

export default function Login({ setToken, setError }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    
    // authenticate the username and password
    const response = await loginUser({
      username,
      password
    });

    if (response.isError){
      setError(response);
    } else {
      setToken({
        "isLoggedIn": true,
        "role": response.role,
        "username": response.username,
      });
    }
  }

  
  return(
    <div className="login-page-wrapper" >
      <div className="login-page-inner-wrapper" >
        <Form onSubmit={handleSubmit}>  
          <h3>Login</h3>
          <Form.Group controlId="formEmail">
            <Form.Label>Username</Form.Label>
            <Form.Control required type="text" placeholder="Enter username" onChange={e => setUserName(e.target.value)} />
          </Form.Group>

          <Form.Group controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control required type="password" placeholder="Enter password" onChange={e => setPassword(e.target.value)}/>
          </Form.Group>
          <Button variant="primary" type="submit" className="btn-block">Submit</Button>
        </Form>
      </div>
    </div>
  )
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
};