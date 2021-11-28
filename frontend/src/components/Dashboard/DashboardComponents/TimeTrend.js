import React from 'react';
import ReactECharts from "echarts-for-react";

export default function TimeTrend({ data }){
    const colors = ['#5470C6', '#91CC75', '#EE6666'];
    const option = {
      color: colors,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: {
        right: '20%'
      },
      toolbox: {
        feature: {
          dataView: { show: true, readOnly: false },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      legend: {
        data: ['Evaporation', 'Precipitation', 'Temperature']
      },
      xAxis: [
        {
          type: 'category',
          axisTick: {
            alignWithLabel: true
          },
          // prettier-ignore
          data: data.xaxis
        }
      ],
      yAxis: [
        {
          type: 'value',
          name: 'GDP Growth Rate',
          position: 'right',
          axisLine: {
            show: true,
            lineStyle: {
              color: colors[0]
            }
          },
          axisLabel: {
            formatter: '{value} ml'
          }
        },
        {
          type: 'value',
          name: 'CPI',
          position: 'right',
          offset: 80,
          axisLine: {
            show: true,
            lineStyle: {
              color: colors[1]
            }
          },
          axisLabel: {
            formatter: '{value} ml'
          }
        },
        {
          type: 'value',
          name: 'Interest Rate',
          position: 'left',
          axisLine: {
            show: true,
            lineStyle: {
              color: colors[2]
            }
          },
          axisLabel: {
            formatter: '{value} °C'
          }
        }
      ],
      series: data.yaxis
    };

    return (
        <ReactECharts option={option}/>
    )
}