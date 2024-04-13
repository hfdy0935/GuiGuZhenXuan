<template>
    <div class="box" ref="box"></div>
</template>

<script setup lang="ts">
import { ref,inject,onMounted } from 'vue'
defineOptions({name: 'Plot'});
let ECharts:any = inject('ECharts');
let box = ref();

let options = {
    title: {
        text: 'ECharts入门示例'
    },
    tooltip: {},
    xAxis: {
        data:  ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
    },
    yAxis: {},
    series: [
        {
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
        }
    ]
}

onMounted(()=>{
    let myChart:any = ECharts.init(box.value);
    myChart.setOption(options);
})


</script>

<style scoped>
.box {
    width: 300px;
    height: 300px;
    background-color: rgba(0,0,0,0.1);
}
</style>