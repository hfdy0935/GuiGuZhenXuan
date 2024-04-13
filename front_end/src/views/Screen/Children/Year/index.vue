<template>
    <div class="box">
        <div class="top">
            <p class="title">年度游客量对比</p>
            <img src="../../images/dataScreen-title.png" alt="">
        </div>
        <div class="chart" ref="chart"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
defineOptions({ name: 'Year' });

let chart = ref();
let myChart: any;
onMounted(() => {
    myChart = echarts.init(chart.value);
    myChart.setOption({
        title: {
            // text: '散点图',
            left: '40%',
            textStyle: {
                color: 'white'
            }
        },
        xAxis: {
            type: 'category',
            show: true,
        },
        yAxis: {
            show: false
        },
        grid: {
            left: 10,
            top: 20,
            right: 10,
            bottom: 30
        },
        series: {
            type: 'scatter',
            data: [33, 88, 21, 9, 88, 234, 113, 1231, 674, 3, 88, 33, 21, 888, 3332, 313, 123, 5, 657, 7],
            //标记图形设置
            symbol: 'diamond',
            symbolSize: 16,
            //图文标签
            label: {
                show: true,
                position: 'top',
                color: 'white',
                fontSize: '11px'
            },
            //散点图标记的颜色
            itemStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0, color: 'red' // 0% 处的颜色
                    },{
                        offset: 0.33, color: 'orange' 
                    },{
                        offset: 0.66, color: 'lightGreen'
                    }, {
                        offset: 1, color: 'blue' // 100% 处的颜色
                    }],
                    global: false // 缺省为 false
                }
            }
        }

    })
});
onBeforeUnmount(() => {
    myChart.dispose();
});
</script>

<style scoped lang="scss">
.box {
    width: 100%;
    height: 100%;
    background: url(../../images/dataScreen-main-cb.png) no-repeat;
    background-size: 100% 100%;
    margin-top: 20px;

    .top {
        .title {
            font-size: 20px;
            color: white;
            position: relative;
            top: 6px;
            left: -30px;
        }
        img{
            position: relative;
            top: 10px;
            left: 8px;
        }
    }
    .chart {
    height: calc(100% - 30px);
  }
}
</style>