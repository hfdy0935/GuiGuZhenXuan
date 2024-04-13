<template>
    <div class="box">
        <div class="top">
            <p class="title">年龄比例</p>
            <p class="bg"></p>
        </div>
        <div class="chart" ref="chart"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts';
defineOptions({ name: 'Age' });

let chart = ref();
let myChart: any;
onMounted(() => {
    myChart = echarts.init(chart.value);
    let option = {
        legend: {
            top: 0,
            right: 10,
            orient: 'vertical',
            textStyle: {
                color: 'white',
                fontSize: 14
            }
        },
        series: [
            {
                name: ' ',
                type: 'pie',
                radius: [30, 110],
                center: ['50%', '50%'],
                roseType: 'area',
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 1
                },
                label: {
                    show: false,
                    position: 'inside',
                    color: 'black'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                data: [
                    { value: 47, name: '0-9' },
                    { value: 38, name: '10-18' },
                    { value: 35, name: '19-27' },
                    { value: 46, name: '28-39' },
                    { value: 48, name: '40-52' },
                    { value: 41, name: '53-60' },
                    { value: 37, name: '61-74' },
                    { value: 39, name: '74+' }
                ],
                grid: {
                    left: 0,
                    top: 0,
                    bottom: 0,
                    right: 0
                }
            }
        ]
    };
    myChart.setOption(option);
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
            margin-left: 20px;
            margin-top: 6px;
        }

        .bg {
            width: 68px;
            height: 7px;
            background: url(../../images/dataScreen-title.png) no-repeat;
            background-size: 100% 100%;
            margin-top: 16px;
            margin-left: 30px;
            transform: scale(1.4);
        }
    }

    .chart {
        width: 100%;
        height: 85%;
    }
}
</style>