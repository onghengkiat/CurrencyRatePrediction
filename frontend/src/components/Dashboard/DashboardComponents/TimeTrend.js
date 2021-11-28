import React from 'react';
import ReactECharts from "echarts-for-react";

export default function TimeTrend({ data }){
    const colors = ['blue', 'green', 'red'];
    const legends = data.map((value, _) => { return value.name;})
    
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
          name: 'GDP Growth Rate',
          scale: true,
          position: 'right',
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
          name: 'CPI',
          scale: true,
          position: 'right',
          offset: 80,
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
          name: 'Interest Rate',
          scale: true,
          position: 'left',
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
        }
      ],
      series: data
    };

    return (
        <ReactECharts option={option}/>
    )
}