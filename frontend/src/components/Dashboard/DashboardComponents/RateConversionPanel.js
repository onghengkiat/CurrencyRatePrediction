import React, { useRef, useState } from 'react';
import Form from "react-bootstrap/Form";
import ErrorComponent from './ErrorComponent';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function RateConversionPanel({ data, chartTitle }){
  const from_currency_value_field = useRef(null);
  const to_currency_code_field = useRef(null);

  const [toValue, setToValue] = useState(null);

  if (data) {
  } else {
    return (
      <Card className="dashboard-chart-inner-container">
        <Card.Body>
          <div className="dashboard-chart-title">{chartTitle}</div>
          <ErrorComponent />
        </Card.Body>
      </Card>
    );
  }

  const handleCalculation = async e => {
      e.preventDefault();
      const myr_to_other = data.myr_to_others[to_currency_code_field.current.value];
      const from_currency_value = Number(from_currency_value_field.current.value);
      const value = from_currency_value * data.to_myr * myr_to_other;
      setToValue(value);
  }

  return (
    <Card className="dashboard-chart-inner-container">
      <Card.Header className="dashboard-chart-rateconversion-header-text">
        {chartTitle}
      </Card.Header>
      <Card.Body>
        <Form>
          <Form.Group>
            <Form.Label>From</Form.Label>
            <Row>
              <Col>
                <Form.Control 
                  required
                  type="number"
                  ref={ from_currency_value_field }
                />
              </Col>
              <Col>
                <Form.Control as="select" disabled custom>
                  <option>USD</option>
                </Form.Control>
              </Col>
            </Row>
          </Form.Group>

          <Form.Group>
            <Form.Label>To</Form.Label>
            <Row>
              <Col>
                <Form.Control 
                  type="number"
                  disabled
                  value={toValue}
                />
              </Col>
              <Col>
                <Form.Control as="select" custom ref={ to_currency_code_field }>
                  {
                      data.currency_list.map((value, _) => {
                          return (  
                              <option value={value}>{value}</option>
                          )
                      })
                  }
                </Form.Control>
              </Col>
            </Row>
          </Form.Group>

        </Form>
      </Card.Body>
      <Card.Footer className="dashboard-chart-rateconversion-footer">
        <Button variant="info" className="responsive dashboard-chart-rateconversion-footer-button" onClick={handleCalculation}>Calculate</Button>
      </Card.Footer>
    </Card>
  )
}