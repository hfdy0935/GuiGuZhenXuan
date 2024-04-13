// 保存左侧菜单折叠状态及更改状态

import { ref } from 'vue'
import { defineStore } from 'pinia'

const useMenuStore = defineStore('menu', () => {
    // 主题颜色
    let color = ref();
    // 是否开启暗黑模式
    let dark = ref(false);
    let t = sessionStorage.getItem('menu');
    let isExpand = ref(t ? ref(JSON.parse(t).isExpand) : true);

    function changeExpandState() {
        isExpand.value = !isExpand.value;
    };
    return {
        color,
        dark,
        isExpand,
        changeExpandState
    }
}, {
    persist: true
}
)

export default useMenuStore