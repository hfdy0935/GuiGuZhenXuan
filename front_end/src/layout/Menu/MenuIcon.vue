<template>
    <el-icon>
        <component :is="iconName"></component>
    </el-icon>
</template>

<script setup lang="ts">
defineProps(['iconName']);
</script>

