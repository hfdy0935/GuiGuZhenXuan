export default [
    {
        name: 'acl',
        path: '/acl',
        component: () => import('@/layout/index.vue'),
        redirect: '/acl/user',
        meta: {
            title: '权限管理',
            hidden: false,
            icon: 'Lock'
        },
        children: [
            {
                name: 'user',
                path: '/acl/user',
                component: () => import('@/views/ACL/User/index.vue'),
                meta: {
                    title: '用户管理',
                    hidden: false,
                    icon: 'User'
                }
            },
            {
                name: 'role',
                path: '/acl/role',
                component: () => import('@/views/ACL/Role/index.vue'),
                meta: {
                    title: '角色管理',
                    hidden: false,
                    icon: 'UserFilled'
                }
            },
            {
                name: 'menu',
                path: '/acl/menu',
                component: () => import('@/views/ACL/Menu/index.vue'),
                meta: {
                    title: '菜单管理',
                    hidden: false,
                    icon: 'SetUp'
                }
            }
        ],
        // beforeEnter(to: any, from: any, next: any) {
        //     if (localStorage.getItem('token')) {
        //         next();
        //         return;
        //     }
        //     next(false);
        // }
    }
]