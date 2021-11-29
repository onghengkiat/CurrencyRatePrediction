import React from 'react';
import ReactECharts from "echarts-for-react";
import ErrorComponent from './ErrorComponent';
import Card from 'react-bootstrap/Card';

export default function PredActual({ data, chartTitle }){
  if (data) {
  } else {
    return (
      <Card className="dashboard-chart-inner-container">
        <Card.Body>
          <div className="dashboard-chart-title">{chartTitle}</div>
          <ErrorComponent />
        </Card.Body>
      </Card>
    )
  }

  const colors = ['blue', '#ff8200'];
  const legends = ['Actual', 'Predicted']
  const markLineData = {
    symbol: 'none',
    lineStyle: {
      type: 'dashed',
      color: 'grey'
    },
    label: {          
      formatter: 'Forecast',
      color: 'grey',
      fontSize: '12px',
    },
    data: [
      {
        name: "forecast",
        xAxis: data.markLinePos,
      }
    ]
  }
  
  const option = {
    color: colors,
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: legends
    },
    grid: {
      containLabel: true,
      bottom: 0,
      left: 0,
      right: 0,
    },
    xAxis: [
      {
        type: 'time',
        axisTick: {
          alignWithLabel: true
        },
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
      }
    ],
    yAxis: {
      type: 'value',
      name: 'Rate',
      scale: true,
      axisLine: {
        show: true,
        lineStyle: {
          color: 'black'
        }
      },
      splitLine: {
        show: false,
      },
      axisLabel: {
        formatter: '{value}'
      }
    },
    series: [{
            name: legends[0],
            type: "line",
            showSymbol: false,
            data: data.actual,
            markLine: markLineData,
        },
        {
            name: legends[1],
            type: "line",
            showSymbol: false,
            data: data.predicted,
            markLine: markLineData,
        },
    ]
  };

  return (
    <Card className="dashboard-chart-inner-container">
      <Card.Body>
        <div className="dashboard-chart-title">{chartTitle}</div>
        <ReactECharts option={option}/>
      </Card.Body>
    </Card>
  )
}