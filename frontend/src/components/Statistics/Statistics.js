import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import { URL_PREFIX } from '../../constants/API';

import './Statistics.css';
import SidePanel from './StatisticsComponents/SidePanel';
import ModelStatistics from './StatisticsComponents/ModelStatistics';
import DatasetStatistics from './StatisticsComponents/DatasetStatistics';
import { BACKEND_SERVER_ERROR } from '../../constants/error';


async function fetchActualPredGraph(currencyCode) {
    return fetch(`${URL_PREFIX}graph/statistic?currency_code=${currencyCode}`, {
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

async function fetchModelPerformanceGraph(currencyCode) {
  return fetch(`${URL_PREFIX}graph/modelperformance?currency_code=${currencyCode}`, {
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

export default function Statistics({ setError, setLoading }){

    const [pic, setPic] = useState();
    const [pic2, setPic2] = useState();
    const [currencyCode, setCurrencyCode] = useState("USD");
    const [currencyList, setCurrencyList] = useState(["USD"]);
    const [statistics, setStatistics] = useState({});
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);

        const response = await fetchModelPerformanceGraph(currencyCode);
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

        const response4 = await fetchActualPredGraph(currencyCode);
        if (response4.isError){
          setError(response4);
        } else {
          const data = response4;
          setPic2(data);
        }

        setLoading(false);
      }
      fetchData();
    }, [currencyCode]);
    
    return (
        <Container fluid>
            <div className="left-content">
                <SidePanel currencyList={ currencyList } setCurrencyCode={ setCurrencyCode }/>
            </div>
            <div className="right-content">
                <DatasetStatistics currency_code={ currencyCode } statistics={ statistics } pic2={ pic2 }/>
                <ModelStatistics pic={ pic }/>
            </div>
        </Container>
    );
}