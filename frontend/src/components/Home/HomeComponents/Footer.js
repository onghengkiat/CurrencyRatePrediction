
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
              src="Enquiry.png"
              alt="Generic placeholder"
            />
          </Media>
        </Col>

        <Col className="footer-col">
          <Row>
            <h5><b>Dataset Information</b></h5>
          </Row>
          <Row>
            The dataset to be used in this project is scraped from 3 different websites which are listed below
          </Row>
          <br/>
          <Row>
            <a href="https://www.bnm.gov.my/web/guest/exchange-rates">
              1. Daily Currency exchange rates compared to Malaysia currency by Bank Negara Malaysia (BNM)
            </a>
          </Row>
          <br/>
          <Row>
            <a href="https://data.imf.org/?sk=4FFB52B2-3653-409A-B471-D47B46D904B5&sId=1485878855236">
              2. Monthly CPI for each of the countries by International Monetary Fund (IMF)
            </a>
          </Row>
          <br/>
          <Row>
            <a href="https://api.worldbank.orConsumer Price Index - IMF Datag/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel">
              3. Yearly GDP Growth for each of the countries by World Bank
            </a>
          </Row>
          {/* <br/>
          <Row>
            <a href="https://api.worldbank.org/v2/en/indicator/FR.INR.RINR?downloadformat=excel">
              4. Yearly Interest Rate for each of the countries by World Bank
            </a>
          </Row> */}
        </Col>

        <Col className="footer-col">
          <Row>
            <h5><b>Source code</b></h5>
          </Row>
          <Row>
            <a href="https://github.com/onghengkiat/CurrencyRatePrediction">
            https://github.com/onghengkiat/CurrencyRatePrediction
            </a>
          </Row>
          <br/>
          <Row>
            <h5><b>Enquiry</b></h5>
          </Row>
          <Row>
            If you have any further questions about this website, you may contact me through
          </Row>
          <br/>
          <Row>
            Email: onghengkiat105@gmail.com
          </Row>
          <br/>
          <Row>
            Whatsapp: 011-11505490
          </Row>
        </Col>
      </Row>
    </Jumbotron>
    )
}