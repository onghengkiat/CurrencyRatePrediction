import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import './BigWord.css';

export default function BigWord(params) {
    const { 
        ChartIcon, 
        ChartIconBackgroundColor,
        ChartHeader,
        ChartBody
    } = params;
    return (
        <Card className="bigword-chart-card">
            <Card.Body style={{"padding":0}}>
                <Container fluid>
                    <Row>
                        <Col xs={3} style={{"background-color":`${ChartIconBackgroundColor}`}}>
                            <ChartIcon className="bigword-chart-icon"/>
                        </Col>
                        <Col xs={9}>
                            <Row><h5 className="bigword-chart-header">{ ChartHeader }</h5></Row>
                            <Row><h3 className="bigword-chart-body">{ ChartBody }</h3></Row>
                        </Col>
                    </Row>
                </Container>
            </Card.Body>
        </Card>
    )
}