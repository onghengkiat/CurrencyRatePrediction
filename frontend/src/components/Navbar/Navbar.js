
import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import './Navbar.css'

export default function NavBar(){
    
    return (
        <Navbar bg="dark" variant="dark" expand="md" sticky="top">
            <Navbar.Brand href="/">
                <img
                width={30}
                height={30}
                className="mr-3"
                src="/logo512.png"
                alt="Generic placeholder"
                />
                CurExc
            </Navbar.Brand>

            <Navbar.Toggle aria-controls="navbar-nav" id="navbar-toggle" />
            <Navbar.Collapse id="navbar-nav" >
                <Nav className="mr-auto">
                    <Nav.Link className="navigation-bar" href="/">Home</Nav.Link>
                    <Nav.Link className="navigation-bar" href="/dataset">Dataset</Nav.Link>
                    <Nav.Link className="navigation-bar" href="/statistic">Statistics</Nav.Link>
                </Nav>

            </Navbar.Collapse>

        </Navbar>
    );
}