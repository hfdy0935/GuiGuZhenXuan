import { createApp } from 'vue';
import ElementPlus from 'element-plus'
// 让ts忽略下一行的检查
// @ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import 'element-plus/dist/index.css'
import App from '@/App.vue'
import pinia from '@/stores'
import { reqUserInfo } from "@/api/user"
import useSuerStore from '@/stores/user'
// 全局组件封装在一起的插件
import globalComponent from '@/components'
// svg插件
import 'virtual:svg-icons-register'
//引入模板的全局的样式
import '@/styles/index.scss'

import router from '@/router/permissions'
// 暗黑模式样式
import 'element-plus/theme-chalk/dark/css-vars.css'
// 按钮权限
import buttonPermission from './directive';

let app = createApp(App);
app.use(ElementPlus, { locale: zhCn }); // 国际化配置
app.use(globalComponent);
app.use(pinia);
// 按钮权限指令
app.directive('btnPermission', buttonPermission);


// markdown相关
// @ts-ignore
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// @ts-ignore
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
// highlightjs
// @ts-ignore
import hljs from 'highlight.js';
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
app.use(VMdPreview);


// 路由使用之前获取用户信息，添加好异步路由
let { saveUserInfo } = useSuerStore();
const pre = async () => {
  const result1: any = await reqUserInfo();
  // 未登录时没有用户信息，这里肯定获取不到，所以加个判断
  // 登录以后刷新时有用户信息，获取到权限，添加好动态路由之后才挂载路由器
  // @ts-ignore
  result1.data?.userInfo && await saveUserInfo(result1.data.userInfo);
  
  app.use(router);
  app.mount('#app');
};
pre();





