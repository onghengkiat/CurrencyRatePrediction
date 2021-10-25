import React from 'react';
import Image from 'react-bootstrap/Image'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import { SiProbot } from 'react-icons/si';


export default function ModelStatistics({ pic }){
    return (
        <div>
            <Row>
                <Container id="dashboard-title" fluid>
                    <Row className="justify-content-between">
                        <Col>
                            <SiProbot id="dashboard-title-icon"/>
                            <h5><b>Predictive Model Performance</b></h5>
                            <h5 className="text-muted"><b>Algorithm: Long Short Term Memory (LSTM)</b></h5>
                        </Col>
                    </Row>
                </Container>
            </Row>
            <Image alt='actual_vs_predicted' src={ pic } className="responsive"/>
        </div>
    );
}