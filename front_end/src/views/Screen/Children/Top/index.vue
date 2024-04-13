<template>
    <div class="top">
        <div class="left">
            <span class="btn" @click="toHome">首页</span>
        </div>
        <div class="center">
            <div class="title">智慧旅游可视化大数据平台</div>
        </div>
        <div class="right">
            <span class="btn">统计报告</span>
            <span class="time">当前时间：{{ time }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
defineOptions({ name: 'Top' });

let router = useRouter();
// 点击返回首页
const toHome = () => {
    router.push({ name: 'home' });
};
let time = ref<string>('');
// @ts-ignore
let timer: any;
onMounted(() => {
    timer = setInterval(() => {
        let temp = new Date();
        let hour = temp.getHours() < 10 ? '0' + temp.getHours() : temp.getHours();
        let minute = temp.getMinutes() < 10 ? '0' + temp.getMinutes() : temp.getMinutes();
        let second = temp.getSeconds() < 10 ? '0' + temp.getSeconds() : temp.getSeconds();
        time.value = temp.getFullYear() + '年' + (temp.getMonth() + 1) + '月' + temp.getDate() + '日    ' + hour + ':' + minute + ':' + second;
    }, 1000);
});
onBeforeUnmount(() => {
    timer = null;
});

</script>

<style scoped lang="scss">
.top {
    width: 100%;
    height: 40px;
    display: flex;

    .left {
        flex: 1;
        background: url(../../images/dataScreen-header-left-bg.png) no-repeat;

        .btn {
            width: 150px;
            height: 40px;
            float: right;
            background: url(../../images/dataScreen-header-btn-bg-l.png);
            background-size: 100% 100%;
            text-align: center;
            line-height: 40px;
            color: #29fcff;
            cursor: pointer;
            user-select: none;
        }
    }

    .center {
        flex: 2;

        .title {
            width: 100%;
            height: 74px;
            line-height: 74px;
            background: url(../../images/dataScreen-header-center-bg.png);
            background-size: 100% 100%;
            text-align: center;
            font-size: 35px;
            color: #29fcff;
        }
    }

    .right {
        flex: 1;
        background: url(../../images//dataScreen-header-right-bg.png) no-repeat;
        background-size: 100% 100%;
        display: flex;
        justify-content: space-between;

        .btn {
            width: 150px;
            height: 40px;
            background: url(../../images/dataScreen-header-btn-bg-r.png) no-repeat;
            text-align: center;
            line-height: 40px;
            color: #29fcff;
            cursor: pointer;
            user-select: none;
        }

        .time {
            color: #29fcff;
            height: 40px;
            line-height: 40px;
            margin-right: 20px;
        }
    }
}
</style>