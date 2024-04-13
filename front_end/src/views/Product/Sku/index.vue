<template>
    <div>
        <el-card>
            <el-table border :data="skuList" stripe highlight-current-row width="100%">
                <el-table-column label="序号" type="index" width="150" align="center"></el-table-column>
                <el-table-column label="名称" show-overflow-tooltip width="250" align="center"
                    prop="name"></el-table-column>
                <el-table-column label="描述" show-overflow-tooltip width="300" align="center"
                    prop="description"></el-table-column>
                <el-table-column label="图片" align="center" width="200">
                    <template #="{ row }">
                        <img :src="row.defaultImage" height="70">
                    </template>
                </el-table-column>
                <el-table-column label="重量" align="center" width="230">

                    <template #="{ row }">
                        {{ row.weight }} g
                    </template>
                </el-table-column>
                <el-table-column label="价格" align="center" width="200">

                    <template #="{ row }">
                        {{ row.price }} 元
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center" width="300" fixed="right">

                    <template #="{ row }">
                        <el-button :icon="row.isShow ? 'Bottom' : 'Top'" :type="row.isShow ? 'warning' : 'success'"
                            :title="row.isShow ? '点击下架' : '点击上架'" @click="changeOneIsShow(row)" v-btnPermission="'上下架'"></el-button>
                        <el-button icon="Edit" type="primary" @click="editOneSku(row)" v-btnPermission="'修改SKU'"></el-button>
                        <el-button icon="InfoFilled" type="info" @click="showDrawer(row)" v-btnPermission="'查看SKU详情'"></el-button>
                        <el-popconfirm title="确定要删除该sku？" @confirm="deleteOneSku(row)">
                            <template #reference>
                                <el-button icon="Delete" type="danger" v-btnPermission="'删除SKU'"></el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" :page-sizes="[5, 10, 15]"
                background v-show="total >= 1" layout="total, sizes, prev, pager, next, jumper" :total="total"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </el-card>
        <!-- 编辑sku的对话框 -->
        <SkuDialog v-model:isSkuDialogShow="isSkuDialogShow" v-model:currentSelectedNum="currentSelectedNum"
            v-model:isSkuAddOrViewOrEdit="isSkuAddOrViewOrEdit" ref="skuDialog"></SkuDialog>
        <!-- 查看详情时的抽屉 -->
        <el-drawer v-model="isDrawerShow" direction="rtl" title="SKU详情">

            <template #default>
                <el-row style="margin:20px 0">
                    <el-col :span="6">名称</el-col>
                    <el-col :span="18">{{ drawerData.name }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col :span="6">价格</el-col>
                    <el-col :span="18">{{ drawerData.price }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col :span="6">重量</el-col>
                    <el-col :span="18">{{ drawerData.weight }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col :span="6">描述</el-col>
                    <el-col :span="18">{{ drawerData.description }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col :span="6">SKU名称</el-col>
                    <el-col :span="18">{{ drawerData.name }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col :span="6">SKU名称</el-col>
                    <el-col :span="18">{{ drawerData.name }}</el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col>平台属性</el-col>
                    <el-col>
                        <el-tag v-for="(item, index) of drawerData.platformProps" :key="index" style="margin: 6px" :type="randomColor()">{{
                item }}</el-tag>
                    </el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col>售卖属性</el-col>
                    <el-col>
                        <el-tag v-for="(item, index) of drawerData.saleProps" :key="index" style="margin: 6px" :type="randomColor()">{{ item
                            }}</el-tag>
                    </el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col>默认图片</el-col>
                    <el-col style="text-align: center">
                        <img :src="drawerData.defaultImage" width="120px"></img>
                    </el-col>
                </el-row>
                <el-row style="margin:20px 0">
                    <el-col>相关图片</el-col><br><br><br>
                    <el-col style="background-color: rgba(0,0,0,0.06);border-radius:10px;">
                        <el-carousel interval="1000" arrow="always" height="150px" trigger="click" type="card">
                            <el-carousel-item v-for="(src, index) in drawerData.detailImages" :key="index">
                                <img :src="src" width="120px">
                            </el-carousel-item>
                        </el-carousel>
                    </el-col>
                </el-row>
            </template>
        </el-drawer>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'
import useProductSkuStore from '@/stores/product/sku'
import useProductSpuStore from '@/stores/product/spu'

let { pageNo, pageSize, total, skuList } = storeToRefs(useProductSkuStore());
let { getSku, changeIsShow, deleteSku, reset } = useProductSkuStore();
let { changeCategoryId } = useProductSpuStore();
let skuDialog = ref();
let isSkuDialogShow = ref(false);
let currentSelectedNum = ref(0); // 点的那个sku在所属三级分类中的序号，从1开始，等于skuNum
let isSkuAddOrViewOrEdit = ref('edit');
// 挂载后获取第一页数据
onMounted(async () => {
    await getSku();
});
// 切换每页sku数量
const handleSizeChange = async () => {
    await getSku();
};
// 切换页数
const handleCurrentChange = async () => {
    await getSku();
};
// 点击上下架某个sku
const changeOneIsShow = async ({ c1id, c2id, c3id, c3num, isShow, skuNum }: any) => {
    let obj = {
        c1id, c2id, c3id, c3num, 'isShow': !isShow, skuNum
    };
    // 发送请求更改上下架状态
    await changeIsShow(obj);
};
// 点击编辑某个sku
const editOneSku = async (row: any) => {
    // c3num是某个三级分类下某个spu的序号，从1开始
    // skuNum是该spu下某个sku的序号，从1开始
    let { c1id, c2id, c3id, c3num, skuNum, name, price, weight, description, defaultImage,
        platformProps: {
            mobile, battery, runMemory, selfMemory, cpuType, screenSize
        },
        saleProps: {
            color, version
        } } = row;
    // 三级分类的id在spu的store中，这里更新一下
    changeCategoryId(c1id, c2id, c3id);
    isSkuDialogShow.value = true;
    currentSelectedNum.value = c3num;
    // 把该sku的详细信息传给SkuDialog组件
    skuDialog.value.name = name;
    skuDialog.value.price = price;
    skuDialog.value.weight = weight;
    skuDialog.value.description = description;
    skuDialog.value.mobile = mobile;
    skuDialog.value.battery = battery;
    skuDialog.value.runMemory = runMemory;
    skuDialog.value.selfMemory = selfMemory;
    skuDialog.value.cpuType = cpuType;
    skuDialog.value.screenSize = screenSize;
    skuDialog.value.color = color;
    skuDialog.value.version = version;
    skuDialog.value.defaultImageUrl = defaultImage;
    skuDialog.value.skuNum = skuNum;
};
// 查看详情，展示抽屉
let isDrawerShow = ref(false);
let drawerData: any = ref({});
let colorList = ['primary', 'success', 'info', 'warning', 'danger'];
let randomColor = () => {
    return colorList[Math.floor(Math.random() * 5)]
};
const showDrawer = (row: any) => {
    isDrawerShow.value = true;
    drawerData.value = row;
    console.log(drawerData.value)
}
// 删除某个sku
const deleteOneSku = async ({ c1id, c2id, c3id, c3num, skuNum }: any) => {
    let obj = {
        c1id, c2id, c3id, c3num, skuNum
    };
    await deleteSku(obj);
};
// 卸载前清空数据
onBeforeUnmount(() => {
    reset();
    // 还得清空spuStore中的三级分类id，不然切到spu时有遗留分类
    changeCategoryId(null, null, null);
});

</script>

<style scoped></style>