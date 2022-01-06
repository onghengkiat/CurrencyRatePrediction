import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { URL_PREFIX } from '../../constants/API';
import timeoutPromise from '../../utils/timeoutPromise';

import './Dashboard.css';
import SidePanel from '../SidePanel/SidePanel';
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
      if (response.status) {
        return response.json();
      } else {
        // case when backend server is not working fine and didn't send any useful info to frontend
        return BACKEND_SERVER_ERROR;
      }
    })
}

async function fetchAlgorithmList() {
  return fetch(`${URL_PREFIX}algorithmlist`, {
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
    if (response.status) {
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
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

async function fetchDashboardActualPred(currency_code, algorithm, include_cpi, include_gdp) {
  return fetch(`${URL_PREFIX}dashboard/actualpred?currency_code=${currency_code}&algorithm=${algorithm}&include_cpi=${include_cpi}&include_gdp=${include_gdp}`, {
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
    if (response.status) {
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
    if (response.status) {
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
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

export default function Dashboard({ token, setError, setLoading }){

    const [currencyCode, setCurrencyCode] = useState("USD");
    const [currencyList, setCurrencyList] = useState(["USD"]);
    const [algorithm, setAlgorithm] = useState("RIDGE");
    const [algorithmList, setAlgorithmList] = useState(["RIDGE"]);
    const [includeCPI, setCPI] = useState(true);
    const [includeGDP, setGDP] = useState(false);
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

        let currencyListResponse = null
        try {
          currencyListResponse = await timeoutPromise(15000, fetchCurrencyList());
        } catch (error) {
          currencyListResponse = BACKEND_SERVER_ERROR;
        }
        if (currencyListResponse.isError){
          setError(currencyListResponse);
        } else {
          const data = currencyListResponse;
          setCurrencyList(data);
        }

        let algorithmListResponse = null
        try {
          algorithmListResponse = await timeoutPromise(15000, fetchAlgorithmList());
        } catch (error) {
          algorithmListResponse = BACKEND_SERVER_ERROR;
        }
        if (algorithmListResponse.isError){
          setError(algorithmListResponse);
        } else {
          const data = algorithmListResponse;
          setAlgorithmList(data);
        }
        
        let dashboardTimeTrendResponse = null
        try {
          dashboardTimeTrendResponse = await timeoutPromise(15000, fetchDashboardTimetrend(currencyCode));
        } catch (error) {
          dashboardTimeTrendResponse = BACKEND_SERVER_ERROR;
        }
        if (dashboardTimeTrendResponse.isError){
          setError(dashboardTimeTrendResponse);
          setTimeTrendData(null);
        } else {
          const data = dashboardTimeTrendResponse;
          setTimeTrendData(data);
        }

        let dashboardActualPredResponse = null
        try {
          dashboardActualPredResponse = await timeoutPromise(15000, fetchDashboardActualPred(currencyCode, algorithm, includeCPI, includeGDP));
        } catch (error) {
          dashboardActualPredResponse = BACKEND_SERVER_ERROR;
        }
        if (dashboardActualPredResponse.isError){
          setError(dashboardActualPredResponse);
          setPredActualData(null);
        } else {
          const data = dashboardActualPredResponse;
          setPredActualData(data);
        }

        let dashboardCurrencyDetailResponse = null
        try {
          dashboardCurrencyDetailResponse = await timeoutPromise(15000, fetchDashboardCurrencyDetail(currencyCode));
        } catch (error) {
          dashboardCurrencyDetailResponse = BACKEND_SERVER_ERROR;
        }
        if (dashboardCurrencyDetailResponse.isError){
          setError(dashboardCurrencyDetailResponse);
          setCurrencyDetailData(null);
        } else {
          const data = dashboardCurrencyDetailResponse;
          setCurrencyDetailData(data);
        }

        let rateConversionResponse = null
        try {
          rateConversionResponse = await timeoutPromise(15000, fetchRateConversion(currencyCode));
        } catch (error) {
          rateConversionResponse = BACKEND_SERVER_ERROR;
        }
        if (rateConversionResponse.isError){
          setError(rateConversionResponse);
          setRateConversionData(null);
        } else {
          const data = rateConversionResponse;
          setRateConversionData(data);
        }

        setLoading(false);
      }
      fetchData();
    }, [currencyCode, algorithm, includeCPI, includeGDP]);
    
  const rightContentClassname = sidePanelIsOpened ? "right-content open" : "right-content";

  return (
      <Container id="dashboard-container" fluid>
        
        <SidePanel token={ token } isOpened={ sidePanelIsOpened } setIsOpened={ setSidePanelIsOpened } currencyList={ currencyList } setCurrencyCode={ setCurrencyCode } algorithmList={ algorithmList } setAlgorithm={ setAlgorithm } setCPI={ setCPI } setGDP={ setGDP }/>

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
                <RateConversionPanel data={ rateConversionData } chartTitle="Rate Conversion" currencyCode={ currencyCode }/>
              </Col>
            </Row>
        </div>
      </Container>
  );
}