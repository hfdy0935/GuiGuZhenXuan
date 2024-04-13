<template>
    <div class="outer">
        <div class="container">
            <img :src="userInfo.avatar">
            <div class="welcome">
                <h1>{{ getTime() }}好，{{ userInfo.username }}</h1>
                <span><i>硅谷甄选运营平台</i></span>
            </div>
        </div>
        <SvgIcon name="welcome" width="600px" height='600px' class="svg"></SvgIcon>
    </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user'

defineOptions({ name: 'Home' });

let { userInfo } = storeToRefs(useUserStore());


// 判断时间
const getTime = () => {
    let hour = new Date().getHours();
    return hour <= 5 ? '凌晨' : hour <= 11 ? '上午' : hour <= 18 ? '下午' : '晚上'
};
</script>

<style scoped lang="scss">
.outer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .container {
        width: 100% !important;
        height: 240px;
        border-radius: 10px;
        box-shadow: 0 0 20px gray;
        margin: 30px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        text-align: center;

        img {
            border-radius: 50%;
            width: 120px;
            height: 120px;
            margin-left: 20px;
        }

        .welcome {
            width: 200px;

            h1 {
                font-size: 26px;
                font-weight: bolder;
                margin-bottom: 20px;
            }

            span {
                font-size: 16px;
                font-style: italic;
                color: rgba(0, 0, 0, 0.5);
            }
        }
    }
}
@media (max-width: 700px){
    .svg{
        width: 300px !important;
    }
}
</style>