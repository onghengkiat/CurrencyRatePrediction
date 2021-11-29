
import Image from 'react-bootstrap/Image';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Introduction(){
    return (
    <Row className="justify-content-center section" sm={2} xs={1}>
      <Col sm lg="4" id="introduction-image">
        <Image
          width={360}
          height={360}
          className="responsive"
          src="logo192.png"
          alt="Generic placeholder"
        />
      </Col>
      <Col sm lg="4" id="introduction">
        <h1>Currency Exchange Rate Prediction (CurEx)</h1>
      </Col>
    </Row>
    )
}