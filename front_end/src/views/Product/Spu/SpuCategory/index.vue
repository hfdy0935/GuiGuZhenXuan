<template>
    <el-card class="card">
        <el-form :inline="true" class="form">
            <el-form-item label="一级分类" class="item">
                <el-select placeholder="请选择分类" clearable v-model.number="category1Id" @change="checkC1">
                    <el-option v-for="(c1, index) in category1List" :key="index" :label="c1" :value="index + 1">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="二级分类" class="item">
                <el-select placeholder="请选择分类" clearable v-model.number="category2Id" @change="checkC2">
                    <el-option v-for="(c2, index) in category2List" :key="index" :label="c2" :value="index + 1"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="三级分类" class="item">
                <el-select placeholder="请选择分类" clearable v-model.number="category3Id" @change="checkC3">
                    <el-option v-for="(c3, index) in category3List" :key="index" :label="c3" :value="index + 1"></el-option>
                </el-select>
            </el-form-item>
        </el-form>
    </el-card>
</template>

<script setup lang="tsx">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import useProductSpuStore from '@/stores/product/spu'
import { reqAttrCategory } from '@/api/product/attr'


defineOptions({ name: 'SpuCategory' });

// 各级分类列表
let { category1List, category2List, category3List } = storeToRefs(useProductSpuStore());
// 选的各级分类id、页数、每页条数
let { category1Id, category2Id, category3Id } = storeToRefs(useProductSpuStore());
// 修改
let { changeCategory1List, changeCategory2List, changeCategory3List, changeCategoryId } = useProductSpuStore();
// 挂载之后发送请求获取c1分类
onMounted(async () => {
    const result: any = await reqAttrCategory({ categoryLevel: 1 });
    changeCategory1List(result.data);
    });
// 点击c1分类
const checkC1 = async () => {
    // 点了清除1级分类
    if (!category1Id.value) {
        changeCategoryId(null, null, null);
        changeCategory2List([]);
        changeCategory3List([]);
        return
    }
    // 正常切换，获取c2分类
    changeCategoryId(category1Id.value, undefined, undefined);
    const result = await reqAttrCategory({
        categoryLevel: 2,
        category1Id: category1Id.value
    });
    changeCategory2List(result.data);
};
// 点击c2分类
const checkC2 = async () => {
    // 点了清除2级分类
    if (!category2Id.value) {
        changeCategoryId(category1Id.value, null, null);
        changeCategory3List([]);
        return
    }
    // 正常切换，获取c3分类
    changeCategoryId(category1Id.value, category2Id.value, undefined);
    const result = await reqAttrCategory({
        categoryLevel: 3,
        category1Id: category1Id.value,
        category2Id: category2Id.value
    });
    changeCategory3List(result.data);
};
// 点击c3分类
const checkC3 = async () => {
    // 点了清除c3分类
    changeCategoryId(category1Id.value, category2Id.value, category3Id.value);
};

</script>

<style scoped lang="scss">
.card {
    width: 100%;
    margin-bottom: 30px;
    height: 10%;
    box-shadow: 0 0 5px black;
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    .item {
        width: 182px;
        margin-right: 60px;
        transform: translateY(30%);
    }
}
</style>