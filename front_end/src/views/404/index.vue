<template>
    <div class="container">
        <img src="@/assets/images/error_images/404.png">
        <p>页面不存在</p>
        <el-button @click="goHome" class="btn">回到首页</el-button>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

defineOptions({ name: '404' });

let router = useRouter();

const goHome = () => {
    router.replace({ name: 'home' })
};
</script>

<style scoped lag="scss">
.container {
    width: 100vw;
    height: 100vh;
    background-color: rgb(98, 191, 227);
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;

    p {
        font-size: 60px;
        color: white;
        position: relative;
        left: -200px;
    }
    .btn{
        transform: scale(1.4);
        position: relative;
        top: 40px;
        left: -200px;
    }

}
</style>