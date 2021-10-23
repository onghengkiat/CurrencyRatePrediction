import { icons } from './TableIcons';
import { columns } from '../../constants/dashboard';
import MaterialTable from 'material-table';
import React, { useEffect, useState } from 'react';
import './Dashboard.css'

async function fetchDashboardData() {
    return fetch(`/dashboard`, {
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
    .then(data => data.message)
    .catch(response => { 
      return response.json()
    })
}

export default function Dashboard({ setError, setSuccess }) {
    const [dashboardData, setData] = useState();
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        const response = await fetchDashboardData();
        if (response.isError){
          // setError(response);
        }else{
          const data = response;
          console.log(data)
          // setData(data);
        }
      }
      fetchData();
      setData([{
          "date": "22 Okt 2021",
          "currency_code": "USD",
          "to_myr": 0.1234,
          "from_myr": 1234.123,
          "rate_changed": 0.12,
          "rate_is_increased": false,
      }])
    }, [setData]);
    
    return (
      <MaterialTable
        data={dashboardData}
        title="Currency Exchange Rate"
        icons={icons}
        columns={columns}
      />
    );
}