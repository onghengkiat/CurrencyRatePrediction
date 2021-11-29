import React from 'react';
import ErrorComponent from './ErrorComponent';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from 'react-bootstrap/Card';

export default function CurrencyDetail({ data, chartTitle }){
    if (data) {
    } else {
      return (
        <Card className="dashboard-chart-inner-container">
          <Card.Body>
            <div className="dashboard-chart-title">{chartTitle}</div>
            <ErrorComponent />
          </Card.Body>
        </Card>
      )
    }

    return (
        <Card className="dashboard-chart-inner-container">
            <Card.Header className="dashboard-chart-detail-header-text">{chartTitle}</Card.Header>
        
            <Card.Body>
                <Row>
                    <Col>
                        <p className="dashboard-chart-detail-text-title">Currency Code</p>
                    </Col>
                    <Col>
                        <p className="dashboard-chart-detail-text">{data.currency_code}</p>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <p className="dashboard-chart-detail-text-title">Country</p>
                    </Col>
                    <Col>
                        <p className="dashboard-chart-detail-text">{data.country}</p>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <p className="dashboard-chart-detail-text-title">From MYR</p>
                    </Col>
                    <Col>
                        <p className="dashboard-chart-detail-text">{data.from_myr}</p>
                    </Col>
                </Row>

                <Row>

                    <Col>
                        <p className="dashboard-chart-detail-text-title">To MYR</p>
                    </Col>
                    <Col>
                        <p className="dashboard-chart-detail-text">{data.to_myr}</p>
                    </Col>
                </Row>
            </Card.Body>
            <Card.Footer className="dashboard-chart-detail-footer-text">
                Updated at <b>{data.updated_date}</b>
            </Card.Footer>
        </Card>
      )
}