import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import { URL_PREFIX } from '../../constants/API';
import timeoutPromise from '../../utils/timeoutPromise';

import './Statistics.css';
import SidePanel from '../SidePanel/SidePanel';
import ModelStatistics from './StatisticsComponents/ModelStatistics';
import DatasetStatistics from './StatisticsComponents/DatasetStatistics';
import { BACKEND_SERVER_ERROR } from '../../constants/error';


async function fetchModelPerformanceGraph(currencyCode, algorithm, include_cpi, include_gdp) {
  return fetch(`${URL_PREFIX}graph/modelperformance?currency_code=${currencyCode}&algorithm=${algorithm}&include_cpi=${include_cpi}&include_gdp=${include_gdp}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      return response;
    }
    throw response;
  })
  .then(data => data.blob())
  .then(blob => URL.createObjectURL(blob))
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

async function fetchModelPerformance(currencyCode, algorithm, include_cpi, include_gdp) {
  return fetch(`${URL_PREFIX}modelperformance?currency_code=${currencyCode}&algorithm=${algorithm}&include_cpi=${include_cpi}&include_gdp=${include_gdp}`, {
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

async function fetchStatistics(currency_code) {
  return fetch(`${URL_PREFIX}statistic?currency_code=${currency_code}`, {
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

export default function Statistics({ token, setError, setLoading }){

    const [pic, setPic] = useState();
    const [currencyCode, setCurrencyCode] = useState("USD");
    const [algorithm, setAlgorithm] = useState("RIDGE");
    const [includeCPI, setCPI] = useState(true);
    const [includeGDP, setGDP] = useState(false);
    const [currencyList, setCurrencyList] = useState(["USD"]);
    const [algorithmList, setAlgorithmList] = useState(["RIDGE"]);
    const [statistics, setStatistics] = useState({});
    const [modelPerformance, setModelPerformance] = useState({});
    const [sidePanelIsOpened, setSidePanelIsOpened] = useState(true);
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);

        let modelPerformanceGraphResponse = null
        try {
          modelPerformanceGraphResponse = await timeoutPromise(5000, fetchModelPerformanceGraph(currencyCode, algorithm, includeCPI, includeGDP));
        } catch (error) {
          modelPerformanceGraphResponse = BACKEND_SERVER_ERROR;
        }
        if (modelPerformanceGraphResponse.isError){
          setError(modelPerformanceGraphResponse);
        } else {
          const data = modelPerformanceGraphResponse;
          setPic(data);
        }

        let currencyListResponse = null
        try {
          currencyListResponse = await timeoutPromise(5000, fetchCurrencyList());
        } catch (error) {
          currencyListResponse = BACKEND_SERVER_ERROR;
        }
        if (currencyListResponse.isError){
          setError(currencyListResponse);
        } else {
          const data = currencyListResponse;
          setCurrencyList(data);
        }

        let statisticsResponse = null
        try {
          statisticsResponse = await timeoutPromise(5000, fetchStatistics(currencyCode));
        } catch (error) {
          statisticsResponse = BACKEND_SERVER_ERROR;
        }
        if (statisticsResponse.isError){
          setError(statisticsResponse);
        } else {
          const data = statisticsResponse;
          setStatistics(data);
        }

        let modelPerformanceResponse = null
        try {
          modelPerformanceResponse = await timeoutPromise(5000, fetchModelPerformance(currencyCode, algorithm, includeCPI, includeGDP));
        } catch (error) {
          modelPerformanceResponse = BACKEND_SERVER_ERROR;
        }
        if (modelPerformanceResponse.isError){
          setError(modelPerformanceResponse);
        } else {
          const data = modelPerformanceResponse;
          setModelPerformance(data);
        }

        let algorithmListResponse = null
        try {
          algorithmListResponse = await timeoutPromise(5000, fetchAlgorithmList());
        } catch (error) {
          algorithmListResponse = BACKEND_SERVER_ERROR;
        }
        if (algorithmListResponse.isError){
          setError(algorithmListResponse);
        } else {
          const data = algorithmListResponse;
          setAlgorithmList(data);
        }

        setLoading(false);
      }
      fetchData();
    }, [currencyCode, algorithm, includeCPI, includeGDP]);
    
    
    const rightContentClassname = sidePanelIsOpened ? "right-content open" : "right-content";

    return (
        <Container id="statistic-container" fluid>
            
            <SidePanel token={ token } isOpened={ sidePanelIsOpened } setIsOpened={ setSidePanelIsOpened } currencyList={ currencyList } setCurrencyCode={ setCurrencyCode } algorithmList={ algorithmList } setAlgorithm={ setAlgorithm } setCPI={ setCPI } setGDP={ setGDP }/>
            
            <div className={rightContentClassname}>
                <DatasetStatistics currencyCode={ currencyCode } statistics={ statistics }/>
                <ModelStatistics pic={ pic } modelPerformance={ modelPerformance } algorithm={ algorithm }/>
            </div>
        </Container>
    );
}