// 存储用户信息
import { ref, reactive } from "vue";
import router from '@/router'
import { asyncRoutes, constRoutes } from '@/router/routes'
import { defineStore } from "pinia";
import type userInfoType from "./types";
import { reqUploadImg } from "@/api/user";
import { reqRolePermission } from "@/api/acl/role";
import { ElMessage } from "element-plus";

// 找到当前某一个权限在异步路由中的对应路由，如果没有则返回false
const filterAsyncRoute = (asyncRoutes: any, userPermissionList: string[]) => {
  return asyncRoutes.filter((item: any) => {
    if (userPermissionList.includes(item.meta.title)) {
      if (item.children && item.children.length > 0) {
        item.children = filterAsyncRoute(item.children, userPermissionList);
      }
      return true
    }
  })
};
// 只有二级菜单没有一级菜单的情况，需要判断并添加对应的一级菜单
const addFirstMenuBySecondMenu = (menu: string[]) => {
  let menuCopy = menu;
  menuCopy.forEach((item: string) => {
    if (item.includes('用户') || item.includes('分配角色')) { menu.push('用户管理') };
    if (item.includes('角色') || item.includes('分配权限')) { menu.push('角色管理') };
    if (item.includes('菜单')) { menu.push('菜单管理') };
    if (menu.includes('用户管理') || menu.includes('角色管理') || menu.includes('菜单管理')) {
      menu.push('权限管理');
    }

    if (item.includes('品牌')) { menu.push('品牌管理') };
    if (item.includes('属性')) { menu.push('属性管理') };
    if (item.includes('SPU') || item === '添加SKU' || item === '查看SKU') { menu.push('SPU管理') };
    if (item === '查看SKU' ||item === '上下架' || item === '修改SKU' || item === '查看SKU详情' || item === '删除SKU') { menu.push('SKU管理') };
    if (menu.includes('品牌管理') || menu.includes('属性管理') || menu.includes('SPU管理') || menu.includes('SKU管理')) {
      menu.push('商品管理');
    };
  });
  let set = new Set(menu);
  return [...set]
};


const useUserStore = defineStore(
  "user",
  () => {
    // 用户信息，顶部导航栏挂载之后才发请求拿到，其中的用户名可以在登录后就拿到
    const userInfo = reactive<any>({});
    // 用户权限
    const userPermission = ref<string[]>([]);
    // token
    const token = ref(localStorage.getItem("token") || "");
    // 保存当前用户的路由，供生成菜单
    let currentRoutes = ref<any>();


    async function saveUserInfo(value: userInfoType) {
      Object.assign(userInfo, value);
      // 保存到localStorage
      localStorage.setItem("username", value.username);
      // 如果是超级管理员，不用获取用户权限，直接开房所有动态路由
      if (value.username === 'admin') {
        asyncRoutes.forEach((item: any) => { router.addRoute(item); });
        currentRoutes.value = [...constRoutes, ...asyncRoutes];
        return Promise.resolve();
      }
      // 其他用户，根据获取到的用户角色获取该用户的权限
      const result: any = await reqRolePermission(userInfo.roleName);
      if (result.code === 200) {
        userPermission.value = result.data;
        // 用户权限列表，需要根据二级菜单添加一级菜单，以防出现只有二级菜单却不显示一级菜单的情况
        let tmpUserPermission = addFirstMenuBySecondMenu(result.data);
        // 过滤出当前权限应有的异步路由
        let r = filterAsyncRoute(asyncRoutes, tmpUserPermission);
        // 挨个添加到路由器中
        r.forEach((item: any) => {
          router.addRoute(item);
        });
        // 更新仓库中的当前总路由
        currentRoutes.value = [...constRoutes, ...r];
        return Promise.resolve();
      }
      return Promise.reject(false);
    }
    function saveToken(tokenStr: string) {
      token.value = tokenStr;
      localStorage.setItem("token", tokenStr);
    }
    // 退出登录时删除用户信息
    function removeUserInfo() {
      Object.keys(userInfo).forEach((item) => {
        delete userInfo[item];
        localStorage.removeItem("username");
      });
    }
    function removeToken() {
      token.value = "";
      localStorage.removeItem("token");
    }
    // 修改仓库中用户头像链接，发送请求更新后端用户头像链接
    async function changeProfilePicture(obj: any) {
      Object.assign(userInfo, { avatar: obj.avatar });
      const r = await fetch(obj.avatar);
      const rr = await r.blob();
      const reqObj = new FormData();
      reqObj.append("file", rr, obj.filename);
      const result: any = await reqUploadImg(reqObj);
      if (result.code === 200 && result.message === "头像上传成功") {
        ElMessage({
          type: "success",
          message: result.message,
        });
      } else {
        ElMessage({
          type: "error",
          message: result.message,
        });
      }
    }

    return {
      userInfo,
      userPermission,
      token,
      currentRoutes,
      saveUserInfo,
      saveToken,
      removeUserInfo,
      removeToken,
      changeProfilePicture,
    };
  },
  { persist: true },
);
export default useUserStore;
