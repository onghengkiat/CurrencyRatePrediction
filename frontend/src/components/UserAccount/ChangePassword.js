import React, { useState } from 'react';
import { URL_PREFIX } from '../../constants/API';
import './ChangePassword.css';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useHistory } from 'react-router-dom';
import { BACKEND_SERVER_ERROR } from '../../constants/error';
import {
  PASSWORD_EDIT_SUCCESS,
} from '../../constants/successMessage';

/////////////////// 
//   API Calls   //
///////////////////

async function changePassword(passwordInfo) {
  return fetch(`${URL_PREFIX}password/change`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(passwordInfo)
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

export default function ChangePassword({ token, setError, setSuccess }) {

  let history = useHistory();
  const [oldPassword, setOldPassword] = useState();
  const [newPassword, setNewPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    
    // authenticate the username and password
    const response = await changePassword({
      username: token.username,
      oldPassword,
      newPassword
    });

    if (response.isError){
        setError(response);
    } else {
        setSuccess(PASSWORD_EDIT_SUCCESS);
        history.push("/profile/view");
    }
  }

  return(
    <div className="password-page-wrapper" >
        <div className="password-page-inner-wrapper" >
            <Form onSubmit={handleSubmit}>  
                <h3>Change Password</h3>
                <Form.Group controlId="formOldPassword">
                <Form.Label>Old Password</Form.Label>
                <Form.Control required type="password" placeholder="Enter old password" onChange={e => setOldPassword(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="formNewPassword">
                <Form.Label>New Password</Form.Label>
                <Form.Control required type="password" placeholder="Enter new password" onChange={e => setNewPassword(e.target.value)}/>
                </Form.Group>
                <Button variant="primary" type="submit" className="btn-block">Submit</Button>
            </Form>
        </div>
    </div>
  )
}
