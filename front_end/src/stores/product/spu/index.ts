import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'
import { reqSpuList, reqDeleteOneSpu, reqAddOneSpu, reqGetOneSpuDetail, reqEditOneSpu, reqBeforeAddSku, reqAddSkuInSpu,reqViewSkuOfSpu } from '@/api/product/spu'
import { addSkuInSpuWithoutCategoryType } from './types'

const useProductSpuStore = defineStore('productSpu', () => {
    // 各级分类列表
    let category1List = ref<any>([]); // 不用初始化，因为挂在之后会发一次请求获取它
    let category2List = ref<any>([]);
    let category3List = ref(<any>[]);
    // 当前三级分类，用v-model绑定
    let category1Id = ref<any>(null);
    let category2Id = ref<any>(null);
    let category3Id = ref<any>(null);
    // sessionStorage中的数据
    let productSpu = sessionStorage.getItem('productSpu');
    // 初始化本地仓库
    if (productSpu) {
        let tmp = JSON.parse(productSpu);
        category2List.value = tmp.category2List;
        category3List.value = tmp.category3List;
        category1Id.value = tmp.category1Id;
        category2Id.value = tmp.category2Id;
        category3Id.value = tmp.category3Id;
    }
    // 更新三级分类列表
    const changeCategory1List = (data: any) => {
        category1List.value = data;
    }
    const changeCategory2List = (data: any) => {
        category2List.value = data;
    };
    const changeCategory3List = (data: any) => {
        category3List.value = data;
    };
    // 更新当前选中的分类id
    const changeCategoryId = async (c1: number | null, c2: number | null, c3: number | null) => {
        category1Id.value = c1;
        category2Id.value = c2;
        category3Id.value = c3;
        // 更新页面
        await updateCurrentPage();
    };

    // 当前页数
    let pageNo = ref(1);
    // 每页显示多少条
    let pageSize = ref(3);
    if (productSpu) {
        let tmp = JSON.parse(productSpu);
        pageNo.value = tmp.pageNo;
        pageSize.value = tmp.pageSize;
    }
    //开始结束位置
    let start = ref(0);
    let end = ref(0);
    // 总数
    let total = ref(0);
    // 改变页数或每页条数
    const changePage = async (n: number, s: number) => {
        pageNo.value = n;
        pageSize.value = s;
        await updateCurrentPage();
    };

    // 属性列表
    let spuList = ref([]);
    // 删除某条属性
    const deleteOneSpu = async (index: number) => {
        const result: any = await reqDeleteOneSpu(
            {
                'category1Id': category1Id.value,
                'category2Id': category2Id.value,
                'category3Id': category3Id.value,
                index
            }
        );
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: '删除成功'
            });
            await updateCurrentPage();
        }
    };
    // 添加一条属性
    const addOneSpu = async (data: FormData) => {
        data.append('category1Id', category1Id.value);
        data.append('category2Id', category2Id.value);
        data.append('category3Id', category3Id.value)
        const result: any = await reqAddOneSpu(data);
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: result.msg
            });
            await updateCurrentPage();
        }
    };
    // 获取某个spu的详细信息
    let oneSpuDetailInfo = ref<any>([]);
    const getOneSpuDetail = async (num: number) => {
        const result: any = await reqGetOneSpuDetail({
            'category1Id': category1Id.value,
            'category2Id': category2Id.value,
            'category3Id': category3Id.value,
            num
        });
        if (result.code === 200) {
            oneSpuDetailInfo.value = result.detail;
        }
    };
    // 清除仓库中保存的某个spu的详细信息
    const clearOneSpuDetail = () => {
        oneSpuDetailInfo.value = [];
    };
    // 编辑一条属性
    const editOneSpu = async (data: FormData) => {
        data.append('category1Id', category1Id.value);
        data.append('category2Id', category2Id.value);
        data.append('category3Id', category3Id.value)
        const result: any = await reqEditOneSpu(data);
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: result.msg
            });
            await updateCurrentPage();
        }
    };

    // 更新本页面，前提：三级分类都选了，发送请求
    const updateCurrentPage = async () => {
        // 清除时
        if (!(category1Id.value && category2Id.value && category3Id.value)) {
            spuList.value = [];
            return
        }
        // 正常获取数据
        const result: any = await reqSpuList({
            category1Id: category1Id.value,
            category2Id: category2Id.value,
            category3Id: category3Id.value,
            pageNo: pageNo.value,
            pageSize: pageSize.value
        });
        total.value = result.total;
        start.value = result.start;
        end.value = result.end;
        spuList.value = result.data;
    };

    // 添加某个spu的sku之前发送请求获取一些数据
    let infoBeforeAddSku = ref([
        { images: [] },
        { isDefault: [] },
        {
            platformProps: {
                battery: [],
                cpuType: [],
                mobile: [],
                runMemory: [],
                screenSize: [],
                selfMemory: []
            }
        }
    ]);
    const getBeforeAddSku = async (num: number) => {
        const result: any = await reqBeforeAddSku({
            'category1Id': category1Id.value,
            'category2Id': category2Id.value,
            'category3Id': category3Id.value,
            num
        });
        if (result.code === 200) {
            infoBeforeAddSku.value = result.result;
        }
    };
    const clearInfoBeforeAddSku = () => {
        infoBeforeAddSku.value = [
            { images: [] },
            { isDefault: [] },
            {
                platformProps: {
                    battery: [],
                    cpuType: [],
                    mobile: [],
                    runMemory: [],
                    screenSize: [],
                    selfMemory: []
                }
            }
        ]
    };
    // 正式添加sku
    const addSku = async (data: addSkuInSpuWithoutCategoryType) => {
        let obj = {
            category1Id: category1Id.value,
            category2Id: category2Id.value,
            category3Id: category3Id.value,
            ...data
        };
        const result: any = await reqAddSkuInSpu(obj);
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: '添加成功'
            });
        }
    };
    // 查看sku，发送请求
    let skuOfOneSpu = ref([]);
    let getSkuOfOneSpu = async (num: number)=>{
        let obj = {
            category1Id: category1Id.value,
            category2Id: category2Id.value,
            category3Id: category3Id.value,
            num
        };
        // 发送请求
        const result: any = await reqViewSkuOfSpu(obj);
        if (result.code === 200) {
            skuOfOneSpu.value = result.data;
        }
    };

    // 重置
    const reset = () => {
        category1List.value = [];
        category2List.value = [];
        category3List.value = [];
        category1Id.value = null;
        category2Id.value = null;
        category3Id.value = null;
        pageNo.value = 1;
        pageSize.value = 3;
        start.value = 0;
        end.value = 0;
        total.value = 0;
        spuList.value = [];
    };

    return {
        category1Id, category1List,
        category2Id, category2List,
        category3Id, category3List,
        changeCategoryId, changeCategory1List, changeCategory2List, changeCategory3List,
        pageNo, pageSize,
        start, end, total, changePage,
        spuList,
        deleteOneSpu, addOneSpu, oneSpuDetailInfo, getOneSpuDetail, clearOneSpuDetail, editOneSpu,
        updateCurrentPage,
        infoBeforeAddSku, getBeforeAddSku, clearInfoBeforeAddSku, addSku,
        skuOfOneSpu,getSkuOfOneSpu,
        reset
    }
}, {
    // 持久化存储
    persist: {
        storage: sessionStorage
    }
});

export default useProductSpuStore