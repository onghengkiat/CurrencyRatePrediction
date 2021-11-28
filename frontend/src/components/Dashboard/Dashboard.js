import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { URL_PREFIX } from '../../constants/API';

import './Dashboard.css';
import ErrorComponent from './DashboardComponents/ErrorComponent';
import SidePanel from './DashboardComponents/SidePanel';
import TimeTrend from './DashboardComponents/TimeTrend';
import { BACKEND_SERVER_ERROR } from '../../constants/error';

async function fetchCurrencyList() {
    return fetch(`${URL_PREFIX}currencylist`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw response;
    })
    .then(data => data.data)
    .catch(response => { 
      // case when backend server is working, and sent frontend the error message
      if (response.isError) {
        return response.json();
      } else {
        // case when backend server is not working fine and didn't send any useful info to frontend
        return BACKEND_SERVER_ERROR;
      }
    })
}

async function fetchDashboardTimetrend(currency_code) {
  return fetch(`${URL_PREFIX}dashboard/timetrend?currency_code=${currency_code}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw response;
  })
  .then(data => data.data)
  .catch(response => { 
    // case when backend server is working, and sent frontend the error message
    if (response.isError) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

export default function Dashboard({ setError, setLoading }){

    const [currencyCode, setCurrencyCode] = useState("USD");
    const [currencyList, setCurrencyList] = useState(["USD"]);
    const [timeTrendData, setTimeTrendData] = useState(null);
    const [sidePanelIsOpened, setSidePanelIsOpened] = useState(true);
    
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);

        const response = await fetchCurrencyList();
        if (response.isError){
          setError(response);
        } else {
          const data = response;
          setCurrencyList(data);
        }

        const response2 = await fetchDashboardTimetrend(currencyCode);
        if (response2.isError){
          setError(response2);
        } else {
          const data = response2;
          setTimeTrendData(data);
        }
        setLoading(false);
      }
      fetchData();
    }, [currencyCode]);
    
  const rightContentClassname = sidePanelIsOpened ? "right-content open" : "right-content";

  return (
      <Container id="dashboard-container" fluid>
        <SidePanel isOpened={ sidePanelIsOpened } setIsOpened={ setSidePanelIsOpened } currencyList={ currencyList } setCurrencyCode={ setCurrencyCode }/>
        <div className={rightContentClassname}>
            <Row lg={2} xs={1} className="dashboard-row">
              <Col lg={4} className="dashboard-chart-outer-container">
                <Card className="dashboard-chart-inner-container">
                  <Card.Body>
                    <div className="dashboard-chart-title">Currency Detail</div>
                  </Card.Body>
                </Card>
              </Col>

              <Col lg={8} className="dashboard-chart-outer-container">
                <Card className="dashboard-chart-inner-container">
                  <Card.Body>
                    <div className="dashboard-chart-title">Time Trend</div>
                    { (!timeTrendData || timeTrendData.length === 0) ? <ErrorComponent /> : <TimeTrend data={ timeTrendData }/>}
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            <Row lg={2} xs={1}>
              <Col lg={8} className="dashboard-chart-outer-container">
                <Card className="dashboard-chart-inner-container">
                  <Card.Body>
                    <div className="dashboard-chart-title">Rates</div>
                  </Card.Body>
                </Card>
              </Col>

              <Col lg={4} className="dashboard-chart-outer-container">
                <Card className="dashboard-chart-inner-container">
                  <Card.Body>
                    <div className="dashboard-chart-title">Rate Conversion</div>
                  </Card.Body>
                </Card>
              </Col>
            </Row>
        </div>
      </Container>
  );
}