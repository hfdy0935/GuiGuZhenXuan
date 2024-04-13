<template>
    <div class="logo">
        <img :src="settings.logo" @click="router.replace('/')" v-show="settings.isLogoShow">
        <Transition name="title">
            <p v-if="isTitleShow">{{ settings.title }}</p>
        </Transition>
    </div>
</template>


<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import useMenuStore from '@/stores/menu'
import { useRouter } from 'vue-router'
import settings from '@/settings'

defineOptions({'name':'Logo'});
const router = useRouter();
let { isExpand } = storeToRefs(useMenuStore());

// 折叠/展开左侧菜单时标题是否显示
let isTitleShow = ref(true);

watch(isExpand, (val: boolean) => {
    isTitleShow.value = val;
}, {immediate: true});


</script>

<style scoped lang="scss">
.logo {
    width: 100%;
    height: $base-menu-logo-height;
    color: white;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    padding: 5px;
    user-select: none;

    img {
        width: 40px;
        height: 40px;
        cursor: pointer;
    }

    p {
        font-size: $base-logo-title-fontSize;
        font-weight: bold;
    }

    @keyframes titleAnimation {
        0% {
            display: none;
        }
        100% {
            display: none;
        }
    }
    .title-enter-active{
        animation: titleAnimation 0.4s;
    }
    .title-leave-active {
        animation: titleAnimation 0.4s reverse;
    }
}

</style>