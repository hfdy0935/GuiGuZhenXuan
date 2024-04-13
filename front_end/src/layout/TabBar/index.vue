<template>
  <div class="tab-bar">
    <!-- 顶部左侧 -->
    <div class="left">
      <div class="expand-fold-icon">
        <MenuIcon
          :iconName="isExpand ? 'Fold' : 'Expand'"
          @click="changeExpandState"
        ></MenuIcon>
      </div>
      <!-- 左侧面包屑 -->
      <BreadCrumb :matchedArray="matchedArray"></BreadCrumb>
    </div>
    <!-- 右侧设置 -->
    <Options></Options>
  </div>
</template>

<script setup lang="ts">
import { toRefs, onMounted, reactive, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import useMenuStore from "@/stores/menu";
import useUserStore from "@/stores/user";
import { reqUserInfo } from "@/api/user";
import MenuIcon from "../Menu/MenuIcon.vue";
import BreadCrumb from "./BreadCrumb/index.vue";
import Options from "./Options/index.vue";
import emitter from "@/utils/emitter";
defineOptions({ name: "TabBar" });
let { isExpand } = storeToRefs(useMenuStore());
let { changeExpandState } = useMenuStore();

// 面包屑导航的显示
let route = toRefs(useRoute());
let matchedArray = route.matched;
let { saveUserInfo, removeUserInfo, removeToken } = useUserStore();
let userInfo = reactive({}); // 获取到的用户信息
let router = useRouter();

// 获取用户信息
const getUserInfo = async () => {
  try {
    const result: any = await reqUserInfo();
    saveUserInfo(result.data.userInfo);
    Object.assign(userInfo, result.data.userInfo);
  } catch (e) {
    // token已过期
    removeUserInfo();
    removeToken();
    router.replace({
      path: "/login",
    });
  }
};
// 绑定获取用户信息事件，确保能更新头像
onMounted(async () => {
  emitter.on("reGetTopBarUserInfo", getUserInfo);
});
onBeforeUnmount(async () => {
  emitter.off("reGetTopBarUserInfo");
});
</script>

<style scoped lang="scss">
.tab-bar {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  user-select: none;

  .left {
    display: flex;
    align-items: center;

    .expand-fold-icon {
      font-size: 30px;
      margin-left: 20px;
      margin-right: 20px;
    }

    @media screen and (max-width: 600px) {
      .expand-fold-icon {
        margin-left: 1px;
        margin-right: 1px;
      }
    }
  }
}
</style>

