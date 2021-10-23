import React from 'react';
import './Home.css'
import Container from 'react-bootstrap/Container';
import Introduction from './HomeComponents/Introduction';
import Features from './HomeComponents/Features';
import Footer from './HomeComponents/Footer';

export default function Home() {
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