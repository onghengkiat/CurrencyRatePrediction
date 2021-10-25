import { icons } from './TableIcons';
import { columns } from '../../constants/dashboard';
import { URL_PREFIX } from '../../constants/API';
import MaterialTable from 'material-table';
import React, { useEffect, useState } from 'react';
import './Dashboard.css'

async function fetchDashboardData() {
    return fetch(`${URL_PREFIX}dashboard`, {
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
        return {
          "isError": true,
          "code": "Error",
          "message": "Something wrong with the backend server",
        }
      }
    })
}

export default function Dashboard({ setError, setSuccess, setLoading }) {
    const [dashboardData, setData] = useState();
  
    // acts as component did mount
    // fetch the data
    useEffect( () => {
      async function fetchData() {
        setLoading(true);
        const response = await fetchDashboardData();
        if (response.isError){
          setError(response);
        } else {
          const data = response;
          setData(data);
        }
        setLoading(false);
      }
      fetchData();
    }, [setData]);

    
    return (
      <MaterialTable
        data={dashboardData}
        title="Currency Exchange Rate"
        icons={icons}
        columns={columns}
        options={{
          grouping: true
        }}
      />
    );
}