export default [
    {
        name: 'home',
        path: '/home',
        component: () => import('@/layout/index.vue'),
        meta: {
            title: '首页',
            hidden: false,
            icon: 'House'
        },
        // redirect: '/home',
        children: [
            {
                path: '/home',
                component: () => import('@/views/Home/index.vue'),
                // redirect: '/home',
                meta: {
                    hidden: true
                }
            }
        ]
    },
    {
        path: '/',
        redirect: '/home',
        meta: {
            title: '首页',
            hidden: true,
            icon: 'House'
        }
    }
]