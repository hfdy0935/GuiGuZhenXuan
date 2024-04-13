<template>
  <div class="container">
    <!-- 左侧菜单 -->
    <div class="left" ref="left">
      <Logo></Logo>
      <el-scrollbar class="scrollbar">
        <el-menu background-color="#001529" text-color="white" active-text-color="orange" :default-active="route.path"
          :collapse="!isExpand" style="border: 0">
          <Menu :menuList="currentRoutes"></Menu>
        </el-menu>
      </el-scrollbar>
    </div>
    <!-- 右侧 -->
    <div class="right" ref="right">
      <!-- 顶部导航 -->
      <div class="topNav">
        <TabBar></TabBar>
      </div>
      <!-- 内容展示区 -->
      <div class="main">
        <Main></Main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import useMenuStore from "@/stores/menu";
import useUserStore from '@/stores/user'
import { useRoute } from "vue-router";
import Logo from "./Logo/index.vue";
import Menu from "./Menu/index.vue";
import Main from "@/views/Main/index.vue";
import TabBar from "./TabBar/index.vue";
defineOptions({ name: "Layout" });

let { currentRoutes } = storeToRefs(useUserStore());
let route = useRoute();
// 左侧菜单
let left = ref();
// 主要内容区
let right = ref();

// 折叠/展开
let { isExpand } = storeToRefs(useMenuStore());

const judgeIsExpand = (val: boolean) => {
  if (val) {
    left.value.style.width = "200px";
    left.value.style.minWidth = "200px";
  } else {
    left.value.style.width = "63px";
    left.value.style.minWidth = "63px";
  }
  right.value.style.width = `calc(100% - ${left.value.style.width})`; // 始终充满右侧区域
};
// 挂在后就根据仓库中的状态处理
onMounted(() => {
  judgeIsExpand(isExpand.value);
});
// 不能用immediate，否则刚开始还没挂载，找不到left和right
watch(isExpand, (val: boolean) => {
  judgeIsExpand(val);
});
</script>

<style scoped lang="scss">
.container {
  width: 100vw;
  height: 100vh;
  display: flex;

  .left {
    width: $base-menu-width;
    max-width: $base-menu-width;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: $base-menu-background;
    transition: all 0.3s linear;

    .scrollbar {
      width: 100%;
      height: calc(100vh - $base-menu-logo-height);

      .scrollbar-item {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50px;
        margin: 10px;
        text-align: center;
        border-radius: 4px;
        background: var(--el-color-primary-light-9);
        color: var(--el-color-primary);
      }
    }
  }

  .right {
    height: 100%;
    display: flex;
    flex-direction: column;
    width: calc(100% - $base-menu-width);

    .topNav {
      width: 100%;
      height: $base-topNav-height;
    }

    .main {
      width: 100%;
      height: calc(100% - $base-topNav-height);
      padding: 20px;
      overflow: auto;
    }
  }
}
</style>
