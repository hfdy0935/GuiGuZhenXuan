<template>
    <div class="box" ref="map">
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { reqChinaMap } from '@/api/screen'
defineOptions({ name: 'Map' });

let map = ref();
let myChart: any;
onMounted(async () => {
    const result: any = await reqChinaMap();
    let data = result;
    echarts.registerMap('china', data);
    myChart = echarts.init(map.value);
    myChart.setOption({
        geo: {
            map: 'china',
            // roam: true,
            left: 10,
            right: 10,
            top: 50,
            bottom: -260,
            label: {
                show: true,
                fontFamily: '华文行楷',
                fontSize: 18
            },
            itemStyle: {
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
                        offset: 0.33, color: 'orange' // 0% 处的颜色
                    },
                    {
                        offset: 0.66, color: 'yellow' // 0% 处的颜色
                    }, {
                        offset: 1, color: 'deepSkyBlue' // 100% 处的颜色
                    }],
                    global: false // 缺省为 false
                },
                opacity: 0.8
            },
            // 高亮
            emphasis: {
                itemStyle: {
                    color: 'cyan'
                },
                label: {
                    fontSize: 30
                }
            }
        },
        grid: {
            left: 0,
            top: 0,
            right: 0,
            bottom: 0
        },
        series: [
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [116.405285, 39.904989],
                            [119.306239, 26.075302]
                        ],
                        lineStyle: {
                            color: 'blue',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'red',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [116.405285, 39.904989],
                            [114.306239, 31.075302]
                        ],
                        lineStyle: {
                            color: 'blue',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'red',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [116.405285, 39.904989],
                            [89.306239, 34.075302]
                        ],
                        lineStyle: {
                            color: 'blue',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'red',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [112.405285, 23.904989],
                            [87.306239, 43.075302]
                        ],
                        lineStyle: {
                            color: 'red',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'blue',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [112.405285, 23.904989],
                            [127.306239, 47.075302]
                        ],
                        lineStyle: {
                            color: 'red',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'blue',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [116.405285, 30.904989],
                            [103.006239, 38.675302]
                        ],
                        lineStyle: {
                            color: 'purple',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'green',
                    symbolSize: 12
                }
            },
            {
                type: 'lines',
                data: [
                    {
                        coords: [
                            [116.405285, 30.904989],
                            [85.006239, 30.675302]
                        ],
                        lineStyle: {
                            color: 'purple',
                            width: 6
                        }
                    }
                ],
                effect: {
                    show: true,
                    symbol: 'arrow',
                    color: 'green',
                    symbolSize: 12
                }
            },
        ]
    })
});
onBeforeUnmount(() => {
    myChart.dispose();
});
</script>