import React from 'react';
import Container from 'react-bootstrap/Container';

export default function ErrorComponent(){

    return (
        <Container className="dashboard-error-component" fluid>
            Something Wrong in Loading the Data. 
            Try to Reload.
        </Container>
    )
}