import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import { URL_PREFIX } from '../../constants/API';

import './Statistics.css';
import SidePanel from './StatisticsComponents/SidePanel';
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
    if (response.isError) {
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
    if (response.isError) {
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
    if (response.isError) {
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
    if (response.isError) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

export default function Statistics({ setError, setLoading }){

    const [pic, setPic] = useState();
    const [currencyCode, setCurrencyCode] = useState("USD");
    const [algorithm, setAlgorithm] = useState("LSTM");
    const [includeCPI, setCPI] = useState(false);
    const [includeGDP, setGDP] = useState(false);
    const [currencyList, setCurrencyList] = useState(["USD"]);
    const [algorithmList, setAlgorithmList] = useState(["LSTM"]);
    const [statistics, setStatistics] = useState({});
    const [modelPerformance, setModelPerformance] = useState({});
    const [sidePanelIsOpened, setSidePanelIsOpened] = useState(true);
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);

        const response = await fetchModelPerformanceGraph(currencyCode, algorithm, includeCPI, includeGDP);
        if (response.isError){
          setError(response);
        } else {
          const data = response;
          setPic(data);
        }

        const response2 = await fetchCurrencyList();
        if (response2.isError){
          setError(response2);
        } else {
          const data = response2;
          setCurrencyList(data);
        }

        const response3 = await fetchStatistics(currencyCode);
        if (response3.isError){
          setError(response3);
        } else {
          const data = response3;
          setStatistics(data);
        }

        const response5 = await fetchModelPerformance(currencyCode, algorithm, includeCPI, includeGDP);
        if (response5.isError){
          setError(response5);
        } else {
          const data = response5;
          setModelPerformance(data);
        }

        const response6 = await fetchAlgorithmList();
        if (response6.isError){
          setError(response6);
        } else {
          const data = response6;
          setAlgorithmList(data);
        }

        setLoading(false);
      }
      fetchData();
    }, [currencyCode, algorithm, includeCPI, includeGDP]);
    
    
    const rightContentClassname = sidePanelIsOpened ? "right-content open" : "right-content";

    return (
        <Container id="statistic-container" fluid>
            
            <SidePanel isOpened={ sidePanelIsOpened } setIsOpened={ setSidePanelIsOpened } currencyList={ currencyList } setCurrencyCode={ setCurrencyCode } algorithmList={ algorithmList } setAlgorithm={ setAlgorithm } setCPI={ setCPI } setGDP={ setGDP }/>
            
            <div className={rightContentClassname}>
                <DatasetStatistics currencyCode={ currencyCode } statistics={ statistics }/>
                <ModelStatistics pic={ pic } modelPerformance={ modelPerformance } algorithm={ algorithm }/>
            </div>
        </Container>
    );
}