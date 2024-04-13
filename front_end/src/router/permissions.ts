// 路由鉴权
import router from '@/router/index'
// @ts-ignore
import nprogress from 'nprogress'
import 'nprogress/nprogress.css'
import useUserStore from '@/stores/user'
import { storeToRefs } from 'pinia'
import pinia from '@/stores'
import { reqLogout } from '@/api/user'


const { token } = storeToRefs(useUserStore(pinia));
let { removeUserInfo, removeToken } = useUserStore();

// 全局前置守卫
router.beforeEach((to: any, _: any, next: any) => {
    document.title = '硅谷甄选-' + to.meta.title;
    nprogress.start();
    // 已登录
    if (token.value) {
        if (to.path === '/login') { next(false); return }
        next();
    } else {
        // 未登录
        // 如果去其他路由，则去登录
        if (to.path !== '/login') {
            next({ path: '/login' });
            reqLogout(localStorage.getItem('username'));
            removeUserInfo();
            removeToken();
            sessionStorage.removeItem('tradeMark');
            return
        }
        next();
    }
});





// 全局后置守卫
router.afterEach(() => {
    nprogress.done();
})

export default router