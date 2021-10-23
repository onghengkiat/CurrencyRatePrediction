
import Media from 'react-bootstrap/Media';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Footer(){
    return (
    <Jumbotron className="section">
      <Row sm={3} xs={1}>
        <Col>
          <Media>
            <img
              width={360}
              height={360}
              className="responsive"
              src="logo192.png"
              alt="Generic placeholder"
            />
          </Media>
        </Col>

        <Col className="footer-col">
          <Row>
            <h5><b>Dataset Information</b></h5>
          </Row>
          <Row>
            The dataset is kindly provided by Bank Negara Malaysia.
          </Row>
          <Row>
            There is an website hosted which shared the data about the currency exchange rate between Malaysia and other countries. The link is attached below:
          </Row>
          <Row>
            <a href="https://www.bnm.gov.my/web/guest/exchange-rates">https://www.bnm.gov.my/web/guest/exchange-rates</a>
          </Row>
        </Col>

        <Col className="footer-col">
          <Row>
            <h5><b>Enquiry</b></h5>
          </Row>
          <Row>
            If you have any further questions about this website, you may contact me through
          </Row>
          <Row>
            Email: onghengkiat105@gmail.com
          </Row>
          <Row>
            Whatsapp: 011-11505490
          </Row>
        </Col>
      </Row>
    </Jumbotron>
    )
}