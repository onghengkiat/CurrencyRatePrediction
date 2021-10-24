import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import './BigNumber.css';

export default function BigNumber(params) {
    const { 
        ChartIcon, 
        ChartIconBackgroundColor,
        ChartIconColor,
        ChartHeader,
        ChartBody
    } = params;
    return (
        <Card className="bignumber-chart-card">
            <Card.Body style={{"padding":0,"background-color":ChartIconBackgroundColor}}>
                <Container fluid>
                    <Row>
                        <Col xs={7}>
                            <Row><p className="bignumber-chart-body"><b>{ ChartBody }</b></p></Row>
                            <Row><h5 className="bignumber-chart-header">{ ChartHeader }</h5></Row>
                        </Col>
                        <Col xs={5}>
                            <ChartIcon className="bignumber-chart-icon" style={{"color":ChartIconColor}}/>
                        </Col>
                    </Row>
                </Container>
            </Card.Body>
        </Card>
    )
}