import React, { useRef } from 'react';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

export default function RateConversionPanel({ data, chartTitle }){
    const currency_code_field = useRef(null);

    const handleSubmit = async e => {
        e.preventDefault();
    }

    return (
        <Card className="dashboard-chart-inner-container">
          <Card.Header>
            <div className="dashboard-chart-title">{chartTitle}</div>
          </Card.Header>
          <Card.Body>
            <Form role="form" onSubmit={handleSubmit}>
                <Form.Group>
                    <Form.Label>Country</Form.Label>
                    <Form.Control as="select" ref={ currency_code_field } custom>
                        [1, 2, 3]
                    </Form.Control>
                </Form.Group>
            </Form>
          </Card.Body>
          <Card.Footer>
            <Button className="responsive">Apply Changes</Button>
          </Card.Footer>
        </Card>
      )
}