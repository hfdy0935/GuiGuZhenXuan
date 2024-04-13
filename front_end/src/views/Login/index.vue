<template>
  <div class="login-container">
    <el-row>
      <el-col :span="12" :xs="50"></el-col>
      <el-col :span="10" :xs="768">
        <el-form class="login-form" :rules="rules" :model="loginForm" ref="loginFormComponent">
          <h1>Hello</h1>
          <h2>欢迎来到硅谷甄选</h2>
          <el-form-item prop="username">
            <el-input :prefix-icon="User" placeholder="用户名" v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" :prefix-icon="Lock" placeholder="密码" v-model="loginForm.password"
              show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="default" class="login-btn" @click="loginEvent"
              :loading="loading">登录</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" size="default" class="login-btn" @click="showDialog">点我获取用户</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <!-- 对话框 -->
    <el-dialog v-model="isDialogShow">
      <v-md-preview :text="mdContent"></v-md-preview>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, toRaw, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElNotification } from "element-plus";
import { User, Lock } from "@element-plus/icons-vue";
import useUserStore from "@/stores/user";
import { reqLogin, reqUserInfo } from "@/api/user";
import type { loginResponseData } from "@/api/user/types";
import rules from "./formRules";
import { reqLoginDocument } from '@/api/document'
defineOptions({ name: "Login" });

let router = useRouter();
let loginForm = reactive({
  username: "",
  password: "",
});

// 判断时间
const getTime = () => {
  let hour = new Date().getHours();
  return hour <= 5
    ? "凌晨"
    : hour <= 11
      ? "上午"
      : hour <= 18
        ? "下午"
        : "晚上";
};
// 保存用户信息
let { saveUserInfo, saveToken } = useUserStore();
// 按钮加载效果
let loading = ref(false);
// 表单组件
let loginFormComponent = ref();
// 登录
async function loginEvent() {
  try {
    // 保证全部表单校验通过再发请求
    await loginFormComponent.value.validate();
    loading.value = true; // 开始加载
    const result: loginResponseData = await reqLogin(toRaw(loginForm));
    if (result.code === 200) {
      // 保存token
      let token = result.data.token as string;
      saveToken(token);
      // 拿到token获取用户信息
      const result1: any = await reqUserInfo();
      // 这里完成发送请求获取用户权限列表和修改路由
      await saveUserInfo(result1.data.userInfo);
      // 成功了再跳转到首页
      if (result1.code === 200) {
        router.replace({
          path: "/home",
        });
        ElNotification({
          type: "success",
          message: "登录成功",
          title: `${getTime()}好`,
        });
        loading.value = false; // 结束加载
        return
      }
    }
  } catch (e) {
    loading.value = false;
    ElMessage({ type: 'error', message: '登录失败' });
  }
  loading.value = false;
}

// 对话框
let isDialogShow = ref(false);
let mdContent = ref('');
const showDialog = async () => {
  const result: any = await reqLoginDocument();
  if (result.code === 200) {
    mdContent = result.data;
    isDialogShow.value = true;
  }
}
</script>

<style scoped lang="scss">
.login-container {
  width: 100vw;
  height: 100vh;
  background: url("@/assets/images/background.jpg") no-repeat;
  background-size: cover;

  .login-form {
    position: relative;
    width: 80%;
    top: 30vh;
    background: url("@/assets/images/login_form.png");
    background-size: cover;
    padding: 40px;
    border-radius: 20px;

    h1 {
      font-size: 40px;
      color: white;
    }

    h2 {
      font-size: 20px;
      color: white;
      margin: 20px 0;
    }

    .login-btn {
      width: 100%;
      background-color: deepskyblue;
      font-size: 18px;
      font-weight: bolder;
    }
  }
}
</style>
