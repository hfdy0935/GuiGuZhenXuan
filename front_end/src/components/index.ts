// 插件，注册全局组件

import SvgIcon from '@/components/SvgIcon/index.vue'
import SkuDialog from '@/components/SkuDialog/index.vue'
// 这里不能用const SvgIcon = import('@/components/SvgIcon/index.vue')
// 也不能这样写app.component('SvgIcon', ()=>import('@/components/SvgIcon/index.vue'))
// 否则没效果

// 图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const allGlobalComponents: any = { SvgIcon, SkuDialog };

export default {
    install(app: any) {
        Object.keys(allGlobalComponents).forEach((index: any) => {
            app.component(index, allGlobalComponents[index]);
        });
        for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
            app.component(key, component);
        }
    }
}