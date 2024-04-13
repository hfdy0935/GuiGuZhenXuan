import { ref } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { reqSku, reqChangeIsShow, reqEditOneSku, reqDeleteOneSku } from '@/api/product/sku'
import { skuIsShowType, deleteOneSkyType } from '@/api/product/sku/types'
import { editOneSkuWithCategoryType } from './types'
import { ElMessage } from 'element-plus'
import useProductSpuStore from '@/stores/product/spu'

const useProductSkuStore = defineStore('productSkuStore', () => {
    let pageNo = ref(1);
    let pageSize = ref(5);
    let total = ref(0);
    let skuList = ref([]);
    let { category1Id: c1id, category2Id: c2id, category3Id: c3id } = storeToRefs(useProductSpuStore());

    // 发送请求获取sku
    const getSku = async () => {
        const result: any = await reqSku({
            pageNo: pageNo.value,
            pageSize: pageSize.value
        });
        if (result.code === 200) {
            total.value = result.data.total;
            skuList.value = result.data.data;
        }
    };
    // 改变上下架状态
    const changeIsShow = async (data: skuIsShowType) => {
        const result: any = await reqChangeIsShow(data);
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: data.isShow ? '上架成功' : '下架成功'
            });
            // 更新
            await getSku();
        }
    };
    // 编辑某个sku
    const editSku = async (data: editOneSkuWithCategoryType) => {
        const result: any = await reqEditOneSku({
            'c1id': c1id.value,
            'c2id': c2id.value,
            'c3id': c3id.value,
            ...data
        });
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: '修改成功'
            });
            // 更新
            await getSku();
        }
    };
    // 删除某个sku
    const deleteSku = async (data: deleteOneSkyType) => {
        const result: any = await reqDeleteOneSku(data);
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: '删除成功'
            });
            // 更新
            await getSku();
        }
    };


    // 重置
    const reset = () => {
        pageNo.value = 1;
        pageSize.value = 5;
        total.value = 0;
        skuList.value = [];
    };

    return {
        pageNo, pageSize, total, skuList, getSku,
        changeIsShow, editSku, deleteSku,
        reset
    }
}, {
    persist: true
});

export default useProductSkuStore
