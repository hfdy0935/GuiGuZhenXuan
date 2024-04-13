<template>
    <div class="box">
        <div class="top">
            <p class="title">游客消费统计</p>
            <img src="../../images/dataScreen-title.png" alt="">
        </div>
        <div class="chart" ref="chart"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
defineOptions({ name: 'Counter' });

let chart = ref();
let myChart: any;
onMounted(() => {
    myChart = echarts.init(chart.value);
    myChart.setOption({
        title: {
            // text: '游客消费统计',
            textStyle: {
                color: 'white'
            }
        },
        radar: {
            // shape: 'circle',
            indicator: [
                { name: '消费', max: 6500 },
                { name: '好感', max: 16000 },
                { name: '出行', max: 30000 },
                { name: '小吃', max: 38000 },
                { name: '爱好', max: 52000 },
                { name: '景点', max: 25000 }
            ]
        },
        series: [
            {
                name: 'Budget vs spending',
                type: 'radar',
                data: [
                    {
                        value: [4200, 3000, 20000, 35000, 50000, 18000],
                        name: '购物'
                    },
                    {
                        value: [5000, 14000, 28000, 26000, 42000, 21000],
                        name: '吃饭'
                    }
                ]
            }
        ]
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
            top: 10px;
            left: -10px;
        }

        img {
            position: relative;
            top: 15px;
            left: 10px;
        }
    }

    .chart {
        height: calc(100% - 30px);
    }
}
</style>