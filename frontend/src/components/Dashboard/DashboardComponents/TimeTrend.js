import React from 'react';
import ReactECharts from "echarts-for-react";
import ErrorComponent from './ErrorComponent';
import Card from 'react-bootstrap/Card';

export default function TimeTrend({ data, chartTitle }){
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

  const colors = ['blue', 'green', 'red'];
  const legends = ["Interest Rate", "GDP Growth Rate", "CPI"]
  
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
    yAxis: [
      {
        type: 'value',
        name: legends[0],
        scale: true,
        position: 'left',
        axisLine: {
          show: true,
          lineStyle: {
            color: colors[0]
          }
        },
        splitLine: {
          show: false,
        },
        axisLabel: {
          formatter: '{value} %'
        }
      },
      {
        type: 'value',
        name: legends[1],
        scale: true,
        position: 'right',
        axisLine: {
          show: true,
          lineStyle: {
            color: colors[1]
          }
        },
        splitLine: {
          show: false,
        },
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: legends[2],
        scale: true,
        position: 'right',
        offset: 80,
        axisLine: {
          show: true,
          lineStyle: {
            color: colors[2]
          }
        },
        splitLine: {
          show: false,
        },
        axisLabel: {
          formatter: '{value} %'
        }
      },
    ],
    series: [{
            name: legends[0],
            type: "line",
            showSymbol: false,
            data: data.interest_rate,
        },
        {
            name: legends[1],
            type: "line",
            showSymbol: false,
            yAxisIndex: 1,
            data: data.cpi,
        },
        {
            name: legends[2],
            type: "line",
            showSymbol: false,
            yAxisIndex: 2,
            data: data.gdp,
        }
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