
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
                                <Accordian.Toggle as={Card.Header} eventKey="1">Predictive Modeling</Accordian.Toggle>
                                <Accordian.Collapse eventKey="1">
                                    <Card.Body>
                                        <Card.Text>
                                            Predictive modeling is a statistical technique using machine learning and data mining to predict and forecast likely future outcomes with the aid of historical and existing data
                                        </Card.Text>
                                    </Card.Body>
                                </Accordian.Collapse>
                            </Card>
                        </Accordian>
                    </Col>

                    <Col>
                        <Accordian>
                            <Card className="feature-card">
                                <Accordian.Toggle as={Card.Header} eventKey="2">Model Transparancy</Accordian.Toggle>
                                <Accordian.Collapse eventKey="2">
                                    <Card.Body>
                                        <Card.Text>
                                            Model is evaluated and the performance evaluation is transparent to the users and displayed in the statistics section
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
                                <Accordian.Toggle as={Card.Header} eventKey="3">Data Analysis</Accordian.Toggle>
                                <Accordian.Collapse eventKey="3">
                                    <Card.Body>
                                        <Card.Text>
                                            Data is presented in different ways to provide more insightful visualizations of data and help in data analysis
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
                                            Data is obtained by webscraping from the website built by a reliable organization which is Bank Negara Malaysia
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