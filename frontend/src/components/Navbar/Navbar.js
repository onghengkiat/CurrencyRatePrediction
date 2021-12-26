
import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Nav from 'react-bootstrap/Nav';
import './Navbar.css'
import { AiOutlineUser } from 'react-icons/ai'
import useWindowDimension from '../../hooks/useWindowDimension';

export default function NavBar({ token }){
    const windowDimensions = useWindowDimension()
    var expanded = windowDimensions.width <= 767;
    var { isLoggedIn, role } = token;
    return (
        <Navbar bg="dark" variant="dark" expand="md" sticky="top">
            <Navbar.Brand href="/">
                <img
                width={30}
                height={30}
                className="mr-3"
                src="/CurrencyExchangeIcon.png"
                alt="Generic placeholder"
                />
                CurEx
            </Navbar.Brand>

            <Navbar.Toggle aria-controls="navbar-nav" id="navbar-toggle" />
            <Navbar.Collapse id="navbar-nav" >
                <Nav className="mr-auto">
                    <Nav.Link className="navigation-bar" href="/">Home</Nav.Link>
                    {isLoggedIn && <Nav.Link className="navigation-bar" href="/dataset">Dataset</Nav.Link>}
                    {isLoggedIn && <Nav.Link className="navigation-bar" href="/statistic">Statistics</Nav.Link>}
                    {isLoggedIn && <Nav.Link className="navigation-bar" href="/dashboard">Dashboard</Nav.Link>}
                    {isLoggedIn && role === "admin" && <Nav.Link className="navigation-bar" href="/user">Users</Nav.Link>}
                </Nav>

                <NavDropdown.Divider />

                {!isLoggedIn && (<Nav>
                     <Nav.Link className="navigation-bar" href="/login">Login</Nav.Link>
                </Nav> )}

                { expanded && isLoggedIn && (<Nav>
                    <Nav.Link className="navigation-bar" href="/profile/view">Profile</Nav.Link>
                    <Nav.Link className="navigation-bar" href="/logout">Logout</Nav.Link>
                </Nav> )}
            </Navbar.Collapse>

            { !expanded && isLoggedIn && (<Nav>
                <NavDropdown title={<AiOutlineUser id="user-icon"/>} id="navbar-dropdown" alignRight> 
                    <NavDropdown.Item className="navigation-bar" href="/profile/view">Profile</NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item className="navigation-bar" href="/logout">Logout</NavDropdown.Item>
                </NavDropdown>
            </Nav> )}

        </Navbar>
    );
}