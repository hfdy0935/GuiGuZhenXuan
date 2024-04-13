<template>
    <div>
        <RouterView v-slot="{ Component }">
            <Transition name="fade" mode="out-in">
                <!-- 防止从数据大屏回来的时候啥也不显示，默认显示主页 -->
                <component :is="Component || Home"></component>
            </Transition>
        </RouterView>
    </div>
</template>


<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import emitter from '@/utils/emitter'
import Home from '@/views/Home/index.vue'
defineOptions({ name: 'Main' });

onMounted(() => {
    emitter.on('refresh', () => {
        location.reload();
    });
});

onUnmounted(() => {
    emitter.off('refresh');
});
</script>

<style scoped lang="scss">
@keyframes fadeAnimation {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

.fade-enter-active {
    animation: fadeAnimation 0.3s;
}

.fade-leave-active {
    animation: fadeAnimation 0.3s reverse;
}
</style>
