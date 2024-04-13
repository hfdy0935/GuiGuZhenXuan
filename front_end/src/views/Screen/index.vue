<template>
    <div class="container">
        <!-- 数据大屏 -->
        <div class="screen" ref="screen">
            <Top></Top>
            <!-- 底部 -->
            <div class="bottom">
                <div class="left">
                    <Tourist class="tourist"></Tourist>
                    <Gender class="gender"></Gender>
                    <Age class="age"></Age>
                </div>
                <div class="middle">
                    <Map class="map"></Map>
                    <Line class="line"></Line>
                </div>
                <div class="right">
                    <Rank class="rank"></Rank>
                    <Year class="year"></Year>
                    <Counter class="counter"></Counter>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Top from './Children/Top/index.vue'
import Tourist from './Children/Tourist/index.vue'
import Age from './Children/Age/index.vue'
import Gender from './Children/Gender/index.vue'
import Map from './Children/Map/index.vue'
import Line from './Children/Line/index.vue'
import Rank from './Children/Rank/index.vue'
import Counter from './Children/Counter/index.vue'
import Year from './Children/Year/index.vue'

defineOptions({ name: 'Screen' });
// 数据大屏dom
let screen = ref();
// 监听视口变化的函数
const viewListener = () => {
    screen.value.style.transform = `scale(${getScale()})  translate(-50%, -50%)`;
}
onMounted(() => {
    viewListener();
    window.addEventListener('resize', viewListener);
});
const getScale = () => {
    const ww = window.innerWidth / 1920;
    const hh = window.innerHeight / 1080;
    return ww < hh ? ww : hh;
};
onBeforeUnmount(() => {
    window.removeEventListener('resize', viewListener);
})
</script>

<style scoped lang="scss">
.container {
    width: 100vw;
    height: 100vh;
    background: url(./images/bg.png);

    .screen {
        width: 1920px;
        height: 1080px;
        position: fixed;
        left: 50%;
        top: 50%;
        transform-origin: left top;


        .bottom {
            display: flex;

            .left {
                flex: 1;
                height: 1040px;
                display: flex;
                flex-direction: column;

                .tourist {
                    flex: 1.5;
                }

                .gender {
                    flex: 1;
                }

                .age {
                    flex: 1;
                }

            }

            .middle {
                flex: 2;
                display: flex;
                box-sizing: border-box;
                flex-direction: column;
                padding-right: 30px;

                .map {
                    flex: 3;
                }

                .line {
                    flex: 1;
                }
            }

            .right {
                flex: 1;
                display: flex;
                flex-direction: column;

                .rank {
                    flex: 1.2;
                }

                .year {
                    flex: 1;
                }

                .counter {
                    flex: 1;
                }
            }
        }
    }
}
</style>