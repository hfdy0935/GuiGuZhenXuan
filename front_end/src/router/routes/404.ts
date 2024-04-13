export default [
    {
        name: '404',
        path: '/404',
        component: () => import('@/views/404/index.vue'),
        meta: {
            title: '404',
            hidden: true,
            icon: 'ShoppingCart'
        }
    },
    {
        name: 'Any',
        path: '/:pathMatch(.*)*',
        redirect: '/404',
        meta: {
            title: '任意路由',
            hidden: true,
            icon: 'Sugar'
        }
    }
]