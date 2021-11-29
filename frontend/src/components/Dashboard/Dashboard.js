import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { URL_PREFIX } from '../../constants/API';

import './Dashboard.css';
import SidePanel from './DashboardComponents/SidePanel';
import CurrencyDetail from './DashboardComponents/CurrencyDetail';
import TimeTrend from './DashboardComponents/TimeTrend';
import PredActual from './DashboardComponents/PredActual';
import RateConversionPanel from './DashboardComponents/RateConversionPanel';
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

async function fetchDashboardActualPred(currency_code) {
  return fetch(`${URL_PREFIX}dashboard/actualpred?currency_code=${currency_code}`, {
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

async function fetchDashboardCurrencyDetail(currency_code) {
  return fetch(`${URL_PREFIX}dashboard/currencydetail?currency_code=${currency_code}`, {
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

async function fetchRateConversion(currency_code) {
  return fetch(`${URL_PREFIX}dashboard/rateconversion?currency_code=${currency_code}`, {
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
    const [predActualData, setPredActualData] = useState(null);
    const [currencyDetailData, setCurrencyDetailData] = useState(null);
    const [rateConversionData, setRateConversionData] = useState(null);
    const [sidePanelIsOpened, setSidePanelIsOpened] = useState(true);
    
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);

        const response = await fetchCurrencyList();
        if (response.isError){
          setError(response);
          setCurrencyList(null);
        } else {
          const data = response;
          setCurrencyList(data);
        }
        
        const response2 = await fetchDashboardTimetrend(currencyCode);
        if (response2.isError){
          setError(response2);
          setTimeTrendData(null);
        } else {
          const data = response2;
          setTimeTrendData(data);
        }

        const response3 = await fetchDashboardActualPred(currencyCode);
        if (response3.isError){
          setError(response3);
          setPredActualData(null);
        } else {
          const data = response3;
          setPredActualData(data);
        }

        const response4 = await fetchDashboardCurrencyDetail(currencyCode);
        if (response4.isError){
          setError(response4);
          setCurrencyDetailData(null);
        } else {
          const data = response4;
          setCurrencyDetailData(data);
        }

        const response5 = await fetchRateConversion(currencyCode);
        if (response5.isError){
          setError(response5);
          setRateConversionData(null);
        } else {
          const data = response5;
          setRateConversionData(data);
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
            <Row md={2} xs={1} className="dashboard-row">
              <Col md={4} className="dashboard-chart-outer-container">
                <CurrencyDetail data={ currencyDetailData } chartTitle="Currency Detail" />
              </Col>

              <Col md={8} className="dashboard-chart-outer-container">
                <TimeTrend data={ timeTrendData } chartTitle="Time Trend"/>
              </Col>
            </Row>

            <Row md={2} xs={1}>
              <Col md={8} className="dashboard-chart-outer-container">
                <PredActual data={ predActualData } chartTitle={`Actual vs Predicted (MYR to ${currencyCode})`}/>
              </Col>

              <Col md={4} className="dashboard-chart-outer-container">
                <RateConversionPanel data={ rateConversionData }chartTitle="Rate Conversion" />
              </Col>
            </Row>
        </div>
      </Container>
  );
}