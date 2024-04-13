<template>
    <el-dialog v-model="isSkuDialogShow" :title="title" width="1000px">
        <!-- 添加sku -->
        <el-card v-if="isFormShow && (isSkuAddOrViewOrEdit == 'add' || isSkuAddOrViewOrEdit == 'edit')">
            <br>
            <el-form label-width="120px">
                <el-form-item label="SKU名称">
                    <el-input v-model="name" placeholder="SKU名称"></el-input>
                </el-form-item>
                <br>
                <el-form-item label="价格（元）">
                    <el-input v-model="price" type="number" placeholder="价格（元）" :min="0"></el-input>
                </el-form-item>
                <br>
                <el-form-item label="重量（克）">
                    <el-input v-model="weight" placeholder="重量（克）"></el-input>
                </el-form-item>
                <br>
                <el-form-item label="SKU描述">
                    <el-input type="textarea" v-model="description" placeholder="SKU描述"></el-input>
                </el-form-item>
                <br>
                <el-form-item label="平台属性">
                    <el-form-item label="手机一级">
                        <el-select v-model="mobile" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.mobile" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="电池容量">
                        <el-select v-model="battery" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.battery" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="运行内存">
                        <el-select v-model="runMemory" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.runMemory" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="机身内存">
                        <el-select v-model="selfMemory" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.selfMemory" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="CPU型号">
                        <el-select v-model="cpuType" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.cpuType" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="屏幕尺寸">
                        <el-select v-model="screenSize" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.platformProps.screenSize" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form-item>
                <br>
                <el-form-item label="售卖属性">
                    <el-form-item label="颜色">
                        <el-select v-model="color" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.saleProps.color" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="版本">
                        <el-select v-model="version" class="select">
                            <el-option v-for="(item, index) in infoBeforeAddSku.saleProps.version" :value="item"
                                :key="index"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form-item>
                <br>
                <el-form-item label="sku图片">
                    <el-table border :data="picInTable">
                        <el-table-column label="序号" width="120" prop="序号" align="center"></el-table-column>
                        <el-table-column label="图片" width="300" align="center">
                            <template #="{ row, $index }">
                                <!-- 预览图 -->
                                <el-image :src="row.图片" style="width: 100px; height: 100px" :zoom-rate="1.2"
                                    :preview-src-list="infoBeforeAddSku.images" fit="cover"
                                    :initial-index="$index"></el-image>
                            </template>
                        </el-table-column>
                        <el-table-column label="名称" width="200" prop="名称" align="center"></el-table-column>
                        <el-table-column label="默认展示" width=200 align="center">

                            <template #="{ $index }">
                                <el-button :type="isImageDefault[$index] === 1 ? 'primary' : ''"
                                    :icon="isImageDefault[$index] === 1 ? 'Check' : ''" class="check"
                                    @click="changeDefaultImage($index)"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-form-item>
            </el-form>
            <br>

            <template #footer>
                <div class="buttons">
                    <el-button @click="cancel">取消</el-button>
                    <el-button type="primary" @click="confirmAddSku">确认</el-button>
                </div>
            </template>
        </el-card>
        <!-- 查看SKU -->
        <el-card v-if="isSkuAddOrViewOrEdit == 'view'">
            <el-table :data="skuOfOneSpu">
                <el-table-column label="序号" prop="序号"></el-table-column>
                <el-table-column label="sku名称" prop="name" align="center"></el-table-column>
                <el-table-column label="sku价格" align="center">

                    <template #="{ row }">
                        {{ row.price }} 元
                    </template>
                </el-table-column>
                <el-table-column label="sku重量" align="center">

                    <template #="{ row }">
                        {{ row.weight }} g
                    </template>
                </el-table-column>
                <el-table-column label="sku图片" align="center">

                    <template #="{ row, $index }">
                        <el-image :src="row.defaultImage" style="width: 100px; height: 100px" :zoom-rate="1.2"
                            :preview-src-list="currentSkuImageUrlList" fit="cover" :initial-index="$index"></el-image>
                    </template>
                </el-table-column>
            </el-table>
            <el-button type="primary" :icon="Back" class="viewReturnBtn" @click="isSkuDialogShow = false">返回</el-button>
        </el-card>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import useProductSpuStore from '@/stores/product/spu'
import useProductSkuStore from '@/stores/product/sku'
import { ElMessage } from 'element-plus'
import { Back } from '@element-plus/icons-vue'

defineOptions({ name: 'SkuDialog' });
let isSkuDialogShow = defineModel('isSkuDialogShow'); // 是否显示
let currentSelectedNum = defineModel('currentSelectedNum'); // 目前选中的序号，从1开始
let isSkuAddOrViewOrEdit = defineModel('isSkuAddOrViewOrEdit'); // 添加还是查看
// 添加某个spu的sku之前
let { infoBeforeAddSku, skuOfOneSpu } = storeToRefs(useProductSpuStore());
let { getBeforeAddSku, clearInfoBeforeAddSku, addSku, getSkuOfOneSpu } = useProductSpuStore();
// 编辑sku
let { editSku } = useProductSkuStore();
let title = computed(() => {
    return isSkuAddOrViewOrEdit.value === 'add' ? '添加SKU' : isSkuAddOrViewOrEdit.value === 'view' ? '查看SKU' : '编辑SKU';
}); // 对话框标题
// 添加的SKU属性
let name = ref('');
let price = ref();
let weight = ref('');
let description = ref('');
// 平台属性
let mobile = ref('');
let battery = ref('');
let runMemory = ref('');
let selfMemory = ref('');
let cpuType = ref('');
let screenSize = ref('');
// 销售属性
let color = ref('');
let version = ref('');
// 是否是默认图片的列表
let isImageDefault: any = ref([]);
// 添加时表格中的图片格式
let picInTable = computed(() => {
    let t: any = [];
    infoBeforeAddSku.value.images.forEach((item: string, index: number) => {
        let obj = {
            '序号': index + 1,
            '图片': item,
            '名称': item.split('spu/')[1].split('?timestamp')[0]
        };
        t.push(obj);
    });
    return t
});

// 初始化所有添加属性
const initAllAttr = () => {
    name.value = '';
    price.value = '';
    weight.value = '';
    description.value = '';
    mobile.value = '';
    battery.value = '';
    runMemory.value = '';
    selfMemory.value = '';
    cpuType.value = '';
    screenSize.value = '';
    color.value = '';
    version.value = '';
};

let isFormShow = ref(false); // 添加中的表单是否显示
let currentSkuImageUrlList = ref([]); // 已有的sku图片url列表
// 根据打开添加/查看对话框发送不同请求
watchEffect(async () => {
    // 点添加、编辑之后发送请求获取对应sku
    if (isSkuDialogShow.value && (isSkuAddOrViewOrEdit.value === 'add' || isSkuAddOrViewOrEdit.value === 'edit')) {
        await getBeforeAddSku(currentSelectedNum.value);
        isFormShow.value = true;
        // 默认的默认图片选择
        isImageDefault.value = infoBeforeAddSku.value.isDefault;
        // 如果编辑sku那儿传来了默认图片的url，则以这个为准
        if (defaultImageUrl.value) {
            isImageDefault.value.fill(0);
            let index = infoBeforeAddSku.value.images.findIndex((item: string) => item === defaultImageUrl.value);
            isImageDefault.value[index] = 1;
            defaultImageUrl.value = '';
        }
    } else if (isSkuDialogShow.value && isSkuAddOrViewOrEdit.value === 'view') {
        // 点查看
        await getSkuOfOneSpu(currentSelectedNum.value);
        currentSkuImageUrlList.value = skuOfOneSpu.value.map((item: any) => item.defaultImage);
    }
    // 对话框不显示时初始化添加中要显示的sku
    if (!isSkuDialogShow.value) {
        initAllAttr();
        isFormShow.value = false;
        clearInfoBeforeAddSku();
        isImageDefault.value = [];
    }
});
// 添加中选择默认图片
const changeDefaultImage = ($index: number) => {
    let tmp = isImageDefault.value[$index];
    isImageDefault.value.fill(0);
    isImageDefault.value[$index] = tmp ? 0 : 1;
};
// 取消添加
const cancel = () => {
    isSkuDialogShow.value = false;
};
// 确认添加
const confirmAddSku = async () => {
    if (!name.value) { ElMessage({ type: 'warning', message: 'sku名称不能为空' }); return }
    if (!price.value) { ElMessage({ type: 'warning', message: '价格不能为空' }); return }
    if (price.value < 0) { ElMessage({ type: 'warning', message: '价格必须是正整数' }); return }
    if (!weight.value) { ElMessage({ type: 'warning', message: '重量不能为空' }); return }
    if (!description.value) { ElMessage({ type: 'warning', message: 'sku描述不能为空' }); return }
    if (!mobile.value) { ElMessage({ type: 'warning', message: '手机一级不能为空' }); return }
    if (!battery.value) { ElMessage({ type: 'warning', message: '电池容量不能为空' }); return }
    if (!runMemory.value) { ElMessage({ type: 'warning', message: '运行内存不能为空' }); return }
    if (!selfMemory.value) { ElMessage({ type: 'warning', message: '机身内存不能为空' }); return }
    if (!cpuType.value) { ElMessage({ type: 'warning', message: 'CPU型号不能为空' }); return }
    if (!screenSize.value) { ElMessage({ type: 'warning', message: '屏幕尺寸不能为空' }); return }
    if (!color.value) { ElMessage({ type: 'warning', message: '颜色不能为空' }); return }
    if (!screenSize.value) { ElMessage({ type: 'warning', message: '版本不能为空' }); return }
    if (!isImageDefault.value.includes(1)) { ElMessage({ type: 'warning', message: '应选择一个默认展示的图片' }); return }
    let obj: any = {
        num: currentSelectedNum.value,
        name: name.value,
        price: price.value,
        weight: weight.value,
        description: description.value,
        platformProps: {
            mobile: mobile.value,
            battery: battery.value,
            runMemory: runMemory.value,
            selfMemory: selfMemory.value,
            cpuType: cpuType.value,
            screenSize: screenSize.value
        },
        saleProps: {
            color: color.value,
            version: version.value
        },
        defaultImage: infoBeforeAddSku.value.images[isImageDefault.value.findIndex((item: number) => item === 1)]
    }
    if (isSkuAddOrViewOrEdit.value === 'add') {
        await addSku(obj);
    } else if (isSkuAddOrViewOrEdit.value === 'edit') {
        obj.skuNum = skuNum.value;
        // 发送请求编辑
        await editSku(obj);
    }

    isSkuDialogShow.value = false;
};

// 供sku中查看某个sku详情时用
let defaultImageUrl = ref(''); // 从编辑sku那传来的默认图片url
let skuNum = ref(0); // 从编辑sku那传来的spu下sku的序号
defineExpose({ name, price, weight, description, mobile, battery, runMemory, selfMemory, cpuType, screenSize, color, version, defaultImageUrl, skuNum });


</script>

<style scoped lang="scss">
.select {
    width: 180px;
    margin: 0 50px 20px 0;
}


.buttons {
    display: flex;
    justify-content: right;
}

.viewImg {
    width: 80px;
}

.viewReturnBtn {
    float: right;
    margin: 20px;
}
</style>