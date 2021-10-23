import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import './ErrorBoundary.css';

export default class ErrorBoundary extends Component {
  state = {
    error: '',
    errorInfo: '',
    hasError: false,
  };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
  }

  render() {
    // show the error boundary object is error occurs
    const { hasError, errorInfo } = this.state;
    return hasError ?
        <Container id="error-boundary-wrapper">
          <Card>
              <Card.Header id="error-boundary-header">
                <b>Error Occured</b>
              </Card.Header>
              <Card.Body>
                Try to reload the page. If error still occurs, contact the administrator for assistant.
              </Card.Body>
              <Card.Footer className="text-center">
                  <Button id="error-boundary-button" href="/">
                      Back to Home Page
                  </Button>
              </Card.Footer>
          </Card>
        </Container>
    : this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.oneOfType([ PropTypes.object, PropTypes.array ]).isRequired,
};
