import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/Container';
import { URL_PREFIX } from '../../constants/API';

import './Dashboard.css';
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

  export default function Dashboard({ setError, setLoading }){
  
      const [currencyCode, setCurrencyCode] = useState("USD");
      const [currencyList, setCurrencyList] = useState(["USD"]);
      const [timeTrendData, setTimeTrendData] = useState({
          "xaxis": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          "yaxis": [
            {
                name: 'GDP Growth Rate',
                type: 'line',
                data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
            },
            {
                name: 'CPI',
                type: 'line',
                yAxisIndex: 1,
                data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
            },
            {
                name: 'Interest Rate',
                type: 'line',
                yAxisIndex: 2,
                data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
            }
      ]});
      
    
      // acts as component did mount
      // fetch the data
      useEffect( () => {
        async function fetchData() {
          setLoading(true);
  
          const response6 = await fetchCurrencyList();
          if (response6.isError){
            setError(response6);
          } else {
            const data = response6;
            setCurrencyList(data);
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
                <TimeTrend data={ timeTrendData }/>
            </div>
          </Container>
      );
  }