import React from 'react';
import ReactECharts from "echarts-for-react";

export default function PredActual({ data }){
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
            formatter: '{value}'
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
      ],
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
              yAxisIndex: 1,
              data: data.predicted,
              markLine: markLineData,
          },
      ]
    };

    return (
        <ReactECharts option={option}/>
    )
}