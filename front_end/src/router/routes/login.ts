export default [
    {
        name: 'login',
        path: '/login',
        component: () => import('@/views/Login/index.vue'),
        meta: {
            title: '登录',
            hidden: true,
            icon: 'Setting'
        }
    }
]