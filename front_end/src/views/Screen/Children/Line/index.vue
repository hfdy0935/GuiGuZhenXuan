<template>
    <div class="box">
        <div class="top">
            <p class="title">未来15天游客数量趋势</p>
            <p class="bg"></p>
        </div>
        <div class="chart" ref="chart"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
defineOptions({ name: 'Line' });

let chart = ref();
let myChart: any;
onMounted(() => {
    myChart = echarts.init(chart.value);
    myChart.setOption({
        title: {
            text: ' '
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            splitLine: false,
            data: ['1号', '2号', '3号', '4号', '5号', '6号', '7号', '8号', '9号', '10号', '11号', '12号', '13号', '14号', '15号']
        },
        yAxis: {
            splitLine: false,
            axisLine: {
                show: true
            },
            axisTick: {
                show: true
            }
        },
        grid: {
            left: 40, top: 0, right: 0, bottom: 30
        },
        series: [
            {
                type: 'line',
                data: [34, 240, 105, 228, 321, 92, 120, 450, 273, 600, 176, 239, 447, 608, 341],
                smooth: true,
                areaStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0, color: 'red' // 0% 处的颜色
                        },
                        {
                            offset: 0.25, color: 'orange' // 0% 处的颜色
                        },
                        {
                            offset: 0.5, color: 'yellow' // 0% 处的颜色
                        }, {
                            offset: 0.75, color: 'deepSkyBlue' // 100% 处的颜色
                        },
                        {
                            offset: 1, color: 'purple' // 100% 处的颜色
                        }],
                        global: false // 缺省为 false
                    },
                }
            }
        ],
        axisPointer: {
            show: true,
            type:'line'
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
    background: url(../../images/dataScreen-main-cb.png);
    background-size: 100% 100%;
    margin: 0 20px;

    .top {
        .title {
            font-size: 20px;
            color: white;
            margin-left: 20px;
            margin-top: 6px;
        }

        .bg {
            width: 68px;
            height: 7px;
            background: url(../../images/dataScreen-title.png) no-repeat;
            background-size: 100% 100%;
            margin-top: 16px;
            margin-left: 80px;
            transform: scale(1.4);
        }
    }

    .chart {
        width: 100%;
        height: calc(100% - 50px);
    }
}
</style>