import React, { useEffect } from 'react';
import './Home.css'
import Container from 'react-bootstrap/Container';
import Introduction from './HomeComponents/Introduction';
import Features from './HomeComponents/Features';
import Footer from './HomeComponents/Footer';

async function pingBackendToBoot() {
  return fetch('${URL_PREFIX}', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export default function Home() {

  useEffect( () => {
    pingBackendToBoot();
  });
  
  return(
    <div>
      <Container fluid>
          <Introduction />
          <Features />
      </Container>  
      <Footer />
    </div>
  );
}