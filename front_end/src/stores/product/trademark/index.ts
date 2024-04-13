import { ref } from 'vue'
import { defineStore } from 'pinia'

const useProductTradeMarkStore = defineStore('productTradeMark', () => {
    // 当前页数
    let pageNo = ref(1);
    const changeCurrentPage = (page: number) => {
        pageNo.value = page;
    };
    // 每页显示多少条
    let pageSize = ref(3);
    const changePageSize = (page: number) => {
        pageSize.value = page;
    };
    return {
        pageNo, changeCurrentPage,
        pageSize, changePageSize
    }
}, {
    // 持久化存储
    persist: {
        storage: sessionStorage
    }
});

export default useProductTradeMarkStore