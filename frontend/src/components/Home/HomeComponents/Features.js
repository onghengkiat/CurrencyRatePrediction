
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Accordian from 'react-bootstrap/Accordion';

export default function Features() {
    return(
        <Row>
            <Container className="section"> 
                <Row>
                    <Col>
                    <h3>
                        <Badge pill variant="info">Features</Badge>{'   '}
                        <span>Whats so special about it?</span>
                    </h3>
                    </Col>
                </Row>
                <Row xs={1} lg={2}>
                    <Col>
                        <Accordian>
                            <Card className="feature-card">
                                <Accordian.Toggle as={Card.Header} eventKey="1">Future Prediction</Accordian.Toggle>
                                <Accordian.Collapse eventKey="1">
                                    <Card.Body>
                                        <Card.Text>
                                            Some quick example text to build on the card Header and make up the bulk of
                                            the card's content.
                                        </Card.Text>
                                    </Card.Body>
                                </Accordian.Collapse>
                            </Card>
                        </Accordian>
                    </Col>

                    <Col>
                        <Accordian>
                            <Card className="feature-card">
                                <Accordian.Toggle as={Card.Header} eventKey="2">Model Transperancy</Accordian.Toggle>
                                <Accordian.Collapse eventKey="2">
                                    <Card.Body>
                                        <Card.Text>
                                            Some quick example text to build on the card Header and make up the bulk of
                                            the card's content.
                                        </Card.Text>
                                    </Card.Body>
                                </Accordian.Collapse>
                            </Card>
                        </Accordian>
                    </Col>

                </Row>
                <Row xs={1} lg={2}>
                    <Col>
                        <Accordian>
                            <Card className="feature-card">
                                <Accordian.Toggle as={Card.Header} eventKey="3">Trend Visualization</Accordian.Toggle>
                                <Accordian.Collapse eventKey="3">
                                    <Card.Body>
                                        <Card.Text>
                                            Some quick example text to build on the card Header and make up the bulk of
                                            the card's content.
                                        </Card.Text>
                                    </Card.Body>
                                </Accordian.Collapse>
                            </Card>
                        </Accordian>
                    </Col>

                    <Col>
                        <Accordian>
                            <Card className="feature-card">
                                <Accordian.Toggle as={Card.Header} eventKey="4">Data Reliable</Accordian.Toggle>
                                <Accordian.Collapse eventKey="4">
                                    <Card.Body>
                                        <Card.Text>
                                            Some quick example text to build on the card Header and make up the bulk of
                                            the card's content.
                                        </Card.Text>
                                    </Card.Body>
                                </Accordian.Collapse>
                            </Card>
                        </Accordian>
                    </Col>
                </Row>
            </Container>
        </Row>
    );
}