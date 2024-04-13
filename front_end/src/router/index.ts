import { createRouter, createWebHashHistory } from 'vue-router'
import { constRoutes } from './routes.ts'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [...constRoutes],
    scrollBehavior() {
        return {
            left: 0,
            top: 0
        }
    }
})



export default router