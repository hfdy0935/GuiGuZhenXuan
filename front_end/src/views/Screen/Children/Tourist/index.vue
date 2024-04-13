<template>
    <div class="box">
        <div class="top">
            <p class="title">实时游客统计</p>
            <p class="bg"></p>
            <p class="total">可预约总量：<span>99999</span>人</p>
        </div>
        <div class="number">
            <span v-for="(item, index) in people" :key="index">{{ item }}</span>
        </div>
        <!-- 图 -->
        <div class="chart" ref="chart">

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted,onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import 'echarts-liquidfill'
defineOptions({ name: 'Tourist' });

let people = ref([2, 1, 5, 9, 0, 8, '人']);
// 图要挂载的元素
let chart = ref();
// 图实例
let myCharts: any;
onMounted(() => {
    myCharts = echarts.init(chart.value);
    // 配置项
    let options = {
        title: { text: ' ' },
        series: {
            type: 'liquidFill',
            waveAnimation: true,
            animationDuration: 1000,
            // animationDurationUpdate: 1000,
            radius: '80%',
            data: [0.6, 0.4, 0.2],
            outline: {
                show: true,
                borderDistance: 10,
                itemStyle:{
                    color: 'red',
                    borderWidth: 15,
                    borderColor: '#294D99'
                }
            }
        }
    };
    myCharts.setOption(options);

});
onBeforeUnmount(()=>{
    myCharts.dispose();
});
</script>

<style scoped lang="scss">
.box {
    background: url(../../images/dataScreen-main-lb.png) no-repeat;
    background-size: 100% 100%;
    margin-top: 10px;

    .top {
        .title {
            font-size: 20px;
            color: white;
            margin-top: 20px;
            margin-left: 30px;
        }

        .bg {
            width: 68px;
            height: 7px;
            background: url(../../images/dataScreen-title.png) no-repeat;
            background-size: 100% 100%;
            margin-top: 16px;
            margin-left: 60px;
            transform: scale(1.5);
        }

        .total {
            float: right;
            color: white;
            margin-right: 30px;
            margin-top: -15px;

            span {
                color: orange;
            }
        }
    }

    .number {
        margin-top: 40px;
        display: flex;
        padding: 10px;

        span {
            flex: 1;
            height: 40px;
            text-align: center;
            line-height: 40px;
            font-size: 26px;
            color: #29fcff;
            background: url(../../images/total.png) no-repeat;
            background-size: 100% 100%;
        }
    }

    .chart {
        width: 100%;
        height: 290px;
    }
}
</style>