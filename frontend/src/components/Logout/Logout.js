import React from 'react';
import './Logout.css'
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

export default function Logout({ token, setToken }) {
    if (token.isLoggedIn){
        setToken({
            "isLoggedIn": false,
            "role": "visitor",
            "username": "",
        });
    }
    
    return(
        <Container id="logout-wrapper">
            <Card>
                <Card.Header id="logout-header">
                    <b>You have been logout</b>
                </Card.Header>
                <Card.Body>
                    Click on the button below to return to the home screen.
                </Card.Body>
                <Card.Footer className="text-center">
                    <Button id="logout-button" href="/">
                        Back to Home Page
                    </Button>
                </Card.Footer>
            </Card>
        </Container>
    )
}
