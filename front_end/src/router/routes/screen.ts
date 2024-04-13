export default [
    {
        name: 'screen',
        path: '/screen',
        component: () => import('@/views/Screen/index.vue'),
        meta: {
            title: '数据大屏',
            hidden: false,
            icon: 'DataBoard'
        }
    }
]