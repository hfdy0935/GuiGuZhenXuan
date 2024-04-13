<template>
    <el-breadcrumb separator-icon="ArrowRight">
        <el-breadcrumb-item v-for="(item, index) in matchedArray" :key="index">
            <div @click="changeRoute(item)">
                <MenuIcon :iconName="item.meta.icon"></MenuIcon>
                <p>{{ item.meta.title }}</p>
            </div>
        </el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script setup lang="ts">
import MenuIcon from '@/layout/Menu/MenuIcon.vue'
import { useRoute,useRouter } from 'vue-router'
defineProps(['matchedArray']);
defineOptions({name: 'BreadCrumb'});

let route = useRoute();
let router = useRouter();
// 点击面包屑导航切换路由
function changeRoute(item: any) {
    // 前后相同路由不跳转
    if(item.path===route.path) return
    router.push({
        path: item.path
    });
}
</script>

<style scoped lang="scss">
div {
    display: flex;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    &:hover {
        color: red;
    }
}

@media screen and (max-width: 740px) {
    p {
        display: none;
    }
    
}
</style>
