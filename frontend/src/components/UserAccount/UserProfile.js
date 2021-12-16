
import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { URL_PREFIX } from '../../constants/API';

import './UserProfile.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { 
    FIELD_NAME,
    FIELD_NAME_TO_BE_DISPLAYED,
    DEFAULT_USER_PROFILE_DATA,
 } from '../../constants/userProfile';
 import { BACKEND_SERVER_ERROR } from '../../constants/error';
 import {
    USER_EDIT_SUCCESS,
 } from '../../constants/successMessage';

/////////////////// 
//   API Calls   //
///////////////////

async function fetchProfile(username) {
    return fetch(`${URL_PREFIX}user?id=${username}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw response;
    })
    .then(data => data.data)
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

async function updateProfile(userInfo) {
    return fetch(`${URL_PREFIX}user`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userInfo)
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

export default function UserProfile({ token, setError, editing=false, setSuccess, setToken }){

    let history = useHistory();
    const [data, setData] = useState(DEFAULT_USER_PROFILE_DATA);

    // act as component did mount
    // fetch the data
    useEffect( () => {
        async function fetchData() {
            const response = await fetchProfile(token.username);
            if (response.isError){
                setError(response);
            }else{
                setData(response);
            }
        }
        fetchData();
    }, [setData]);

    const handleChange = e => {
        const key = e.target.id;
        const value = e.target.value;
        setData({
            ...data,
            [key]: value
        })
    };

    const handleSubmit = async e => {
        e.preventDefault();
        // authenticate the username and password
        const response = await updateProfile({
            "condition": {
                "username": token["username"],
            },
            "data": data,
        });

        if (response.isError){
            setError(response);
        } else {
            // setToken({
            //   "isLoggedIn": true,
            //   "role": token["role"],
            //   "username": data["username"],
            // });
            setToken({
                "isLoggedIn": true,
                "role": token["role"],
                "username": token["username"],
            });
            setSuccess(USER_EDIT_SUCCESS);
            history.push("/profile/view");
        }
    };

    return (
        <Container id="user-profile-container" className="d-flex flex-column align-items-center">
            <Col md={8}>
                <Card>
                    <Card.Body>
                        <div className="d-flex flex-column align-items-center text-center">
                            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Admin" className="rounded-circle" width="150"/>
                            <div className="mt-3">
                                <h4>{data["fullname"]}</h4>
                            </div>
                        </div>

                        {FIELD_NAME.map( (value, _) => (
                            <div>
                                <Row>
                                    <Col sm={3}>
                                        <h6>{FIELD_NAME_TO_BE_DISPLAYED[value]}</h6>
                                    </Col>
                                    <Col sm={9} className="secondary-text">
                                        {
                                        // role is not editable in the profile page
                                        editing && value !== "role"? 
                                        <Form.Control required id={value} type="text" value={data[value]} onChange={handleChange}/>
                                        :
                                        data[value]
                                        }
                                    </Col>
                                </Row>
                                <hr/>
                            </div>
                        ))}
                        {
                        editing?
                        <Row>
                            <Col>
                                <Button variant="primary" type="submit" className="btn-block" onClick={handleSubmit}>Save Changes</Button>
                            </Col>
                        </Row>
                        :
                        <Row>
                            <Col xl={1} sm={2} className="user-profile-button">
                                <Button variant="info" href="/profile/edit">Edit</Button>
                            </Col>
                            <Col xl={11} sm={10} className="user-profile-button">
                                <Button variant="info" href="/password">Change Password</Button>
                            </Col>
                        </Row>
                        }
                    </Card.Body>
                </Card>
            </Col>
        </Container>
    )
}