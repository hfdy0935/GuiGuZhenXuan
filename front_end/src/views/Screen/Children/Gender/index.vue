<template>
    <div class="box">
        <div class="top">
            <p class="title">男女比例</p>
            <p class="bg"></p>
        </div>
        <div class="bottom">
            <div class="man">
                <img src="../../images/man.png">
            </div>
            <div class="woman">
                <img src="../../images/woman.png">
            </div>
        </div>
        <div class="rate">
            <p>男 58%</p>
            <p>女 42%</p>
        </div>
        <div class="chart" ref="chart">

        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
defineOptions({ name: 'Gender' });

let chart = ref();
let myChart: any;
onMounted(() => {
    myChart = echarts.init(chart.value);
    myChart.setOption({
        title: {
            text: ' ',
            textStyle: { color: 'skyblue' },
            left: '40%'
        },
        xAxis: {
            show: false,
            min: 0,
            max: 100
        },
        yAxis: {
            show: false,
            type: 'category'
        },
        series: [
            {
                type: 'bar',
                data: [58],
                barWidth: 20,
                z: 100,
                itemStyle: {
                    color: '#007AFE',
                    borderRadius: 20
                }
            },
            {
                type: 'bar',
                data: [100],
                barWidth: 20,
                barGap: '-100%',
                itemStyle: {
                    color: '#FF4B7A',
                    borderRadius: 20
                }
            }
        ],
        grid: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
        }
    });
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

    .bottom {
        display: flex;
        justify-content: center;
        align-items: center;

        .man {
            margin: 20px;
            width: 111px;
            height: 115px;
            text-align: center;
            background: url(../../images/man-bg.png) no-repeat;
            background-size: 100% 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .woman {
            margin: 20px;
            width: 111px;
            height: 115px;
            text-align: center;
            line-height: 115px;
            background: url(../../images/woman-bg.png) no-repeat;
            background-size: 100% 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    }

    .rate {
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 26px;
        margin-left: 50px;
        margin-right: 50px;
    }

    .chart {
        width: 80%;
        height: 50px;
        margin: 0 auto;
    }
}
</style>