import { icons } from './TableIcons';
import { URL_PREFIX } from '../../constants/API';
import MaterialTable from 'material-table';
import React, { useEffect, useState } from 'react';
import './Dataset.css'
import { BACKEND_SERVER_ERROR } from '../../constants/error';

async function fetchDashboardData() {
    return fetch(`${URL_PREFIX}dataset`, {
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

export default function Dataset({ setError, setSuccess, setLoading }) {
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
        columns={[{
          title: "Date",
          field: "date",
          type: "date",
        },
        {
          title: "Currency Code",
          field: "currency_code",
        },
    
        {
          title: "CPI (Prev Month)",
          field: "cpi",
        },
        {
          title: "GDP Growth Rate (Prev Year)",
          field: "gdp",
        },
        // {
        //   title: "Interest Rate (Prev Year)",
        //   field: "interest_rate",
        // },
        {
          title: "To MYR",
          field: "to_myr",
        },
        {
          title: "From MYR",
          field: "from_myr",
        }]}
        options={{
          filtering: true
        }}
      />
    );
}