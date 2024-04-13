<template>
    <svg :style="{ width: width, height: height }">
        <use :xlink:href="prefix + name" :fill="color"></use>
    </svg>
</template>

<script setup lang="ts">
defineOptions({name: 'SvgIcon'});
defineProps({
    // 前缀
    prefix: {
        type: String,
        default: '#icon-'
    },
    // 图标名
    name: String,
    // 颜色
    color: {
        type: String,
        default: ''
    },
    // 宽度
    width: {
        type: String,
        default: '16px'
    },
    // 高度
    height: {
        type: String,
        default: '16px'
    } 
})
</script>
