import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'
import { reqAttrList, reqDeleteOneAttr, reqAddOneAttr, reqEditOneAttr } from '@/api/product/attr'
import { addOneAttrType, editOneAttrType } from './types'

const useProductAttrStore = defineStore('productAttr', () => {
    // 各级分类列表
    let category1List = ref<any>([]); // 不用初始化，因为挂在之后会发一次请求获取它
    let category2List = ref<any>([]);
    let category3List = ref(<any>[]);
    // 当前三级分类，用v-model绑定
    let category1Id = ref<any>(null);
    let category2Id = ref<any>(null);
    let category3Id = ref<any>(null);
    // sessionStorage中的数据
    let productAttr = sessionStorage.getItem('productAttr');
    // 初始化本地仓库
    if (productAttr) {
        let tmp = JSON.parse(productAttr);
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
    if (productAttr) {
        let tmp = JSON.parse(productAttr);
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
    let attrList = ref([]);
    // 删除某条属性
    const deleteOneAttr = async (index: number) => {
        const result: any = await reqDeleteOneAttr(
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
    const addOneAttr = async (data: addOneAttrType) => {
        const result: any = await reqAddOneAttr({
            'category1Id': category1Id.value,
            'category2Id': category2Id.value,
            'category3Id': category3Id.value,
            ...data
        });
        if (result.code === 200) {
            ElMessage({
                type: 'success',
                message: result.msg
            });
            await updateCurrentPage();
        }
    };
    // 编辑一条属性
    const editOneAttr = async (data: editOneAttrType) => {
        const result: any = await reqEditOneAttr({
            'category1Id': category1Id.value,
            'category2Id': category2Id.value,
            'category3Id': category3Id.value,
            ...data
        });
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
            attrList.value = [];
            return
        }
        // 正常获取数据
        const result: any = await reqAttrList({
            category1Id: category1Id.value,
            category2Id: category2Id.value,
            category3Id: category3Id.value,
            pageNo: pageNo.value,
            pageSize: pageSize.value
        });
        total.value = result.total;
        start.value = result.start;
        end.value = result.end;
        attrList.value = result.data;
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
        attrList.value = [];
    };

    return {
        category1Id, category1List,
        category2Id, category2List,
        category3Id, category3List,
        changeCategoryId, changeCategory1List, changeCategory2List, changeCategory3List,
        pageNo, pageSize,
        start, end, total,changePage,
        attrList,
        deleteOneAttr, addOneAttr, editOneAttr,
        updateCurrentPage,
        reset
    }
}, {
    // 持久化存储
    persist: {
        storage: sessionStorage
    }
});

export default useProductAttrStore