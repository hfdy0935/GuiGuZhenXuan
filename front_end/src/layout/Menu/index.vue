<template>
    <template v-for="item in menuList" :key="item.path">
        <!-- 没有子路由 -->
        <el-menu-item v-if="!item.children && !item.meta.hidden" :index="item.path" @click="changeRoute">
            <MenuIcon :iconName="item.meta.icon"></MenuIcon>
            <template #title>
                {{ item.meta.title }}
            </template>
        </el-menu-item>
        <!-- 有子路由，子路由至少有一个显示，则它本身是el-sub-menu，能显示下级，并递归调用组件 -->
        <el-sub-menu v-if="item.children && !item.meta.hidden && checkChildren(item)" :index="item.path">
            <template #title>
                <MenuIcon :iconName="item.meta.icon"></MenuIcon>
                <span>{{ item.meta.title }}</span>
            </template>

            <Menu :menuList="item.children"></Menu>
        </el-sub-menu>
        <!-- 有子组件，子路由都不显示，则它本身是el-menu-item，不能显示下级 -->
        <el-menu-item v-if="item.children && !item.meta.hidden && !checkChildren(item)" :index="item.path" @click="changeRoute">
            <MenuIcon :iconName="item.meta.icon"></MenuIcon>
            <template #title>
                <span>{{ item.meta.title }}</span>
            </template>
        </el-menu-item>
    </template>
</template>

<script setup lang="ts">
import { isProxy } from 'vue'
import type { RouteRecordRaw } from 'vue-router'
import { useRouter } from 'vue-router'
import MenuIcon from './MenuIcon.vue'

defineOptions({name: 'Menu'});
let router = useRouter();
type RouteRecordRaw = typeof RouteRecordRaw;
// 获取父组件传来的路由数组
defineProps(['menuList']);

// 检查子路由是否都设置了hidden: true
function checkChildren(item: RouteRecordRaw) {
    return item.children.findIndex((k: RouteRecordRaw) => k.meta.hidden === false) === -1 ? false : true
};
// 点击菜单跳转路由
function changeRoute(value: any) {
    if (!isProxy(value)) return
    router.push(value.index);
};

</script>

<style scoped>
div {
    color: white;
}
</style>