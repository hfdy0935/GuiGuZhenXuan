<template>
    <div class="container">
        <!-- 三级分类 -->
        <SpuCategory></SpuCategory>
        <!-- 添加、编辑，这里改成切换 -->
        <el-card v-show="currentShowType==='addOrEdit'" :title="isAddOrEdit" width="1000px">
            <el-form>
                <el-form-item label="SPU名称">
                    <el-input v-model="addSpuName" placeholder="输入SPU名称" :prefix-icon="Goods"></el-input>
                </el-form-item>
                <el-form-item label="SPU描述">
                    <el-input v-model="addSpuDescription" placeholder="输入SPU描述" type="textarea" :rows="2"></el-input>
                </el-form-item>
                <el-form-item label="SPU图片">
                    <el-upload action="#" list-type="picture-card" :auto-upload="false" class="upload" ref="uploadImage"
                        :on-remove="handleRemove" :on-preview="handlePictureCardPreview" :on-change="uploadStateChange"
                        v-model:file-list="uploadImageNameAndUrlList">
                        <el-icon>
                            <Plus />
                        </el-icon>
                    </el-upload>
                    <!-- 预览图 -->
                    <el-dialog v-model="isPreviewDialogShow">
                        <img w-full :src="currentImageUrl" width="600">
                    </el-dialog>
                </el-form-item>
                <el-form-item label="SPU标签">
                    <el-table :data="addSpuPropsList" style="margin: 10px 0;" border stripe>
                        <el-table-column label="序号" width="100" prop="序号" align="center"></el-table-column>
                        <el-table-column label="属性" width="150" prop="属性" align=center>
                            <template #="{ row }">
                                <el-input v-model="addPropInputContent[row.序号 - 1]"
                                    @blur="addPropInputBlur(row.序号)"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column label="标签" width="550" prop="标签" align="center">
                            <template #="{ row }">
                                <!-- 每个标签 -->
                                <el-tag v-for="(tag, index) in row.标签" :key="index" :type="reflection[row.标签颜色[index]]"
                                    closable @close="removeOneTag(row.序号, index)" class="oneTag">
                                    <!-- 这里用@，不用: -->
                                    {{ tag }}
                                </el-tag>
                                <!-- 添加标签时的输入框 -->
                                <el-input v-if="isAddTagInputShow[row.序号 - 1]" class="addOneTagInput"
                                    v-model="addTagInputContent[row.序号 - 1]" @blur="addTagInputBlur(row.序号)"
                                    ref="input"></el-input>
                                <!-- 添加一个标签按钮 -->
                                <el-dropdown>
                                    <el-button class="addOneTagPlus">+</el-button>
                                    <!-- 下来菜单选标签颜色 -->
                                    <template #dropdown>
                                        <el-dropdown-menu>
                                            <el-dropdown-item v-for="(color, colorIndex) in reflection"
                                                @click="showInputAndSendColor(row.序号, colorIndex)" :key="colorIndex">
                                                <el-button :type="color">{{ color }}</el-button>
                                            </el-dropdown-item>
                                        </el-dropdown-menu>
                                    </template>
                                </el-dropdown>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="100" align="center">
                            <template #default="{ row }">
                                <el-button type="danger" @click="deleteOneSpuTag(row.序号)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-button type="primary" :icon="Plus" @click="addOneSpuProp">添加一项</el-button>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="cancelAndSendReq">取消</el-button>
                <el-button type="primary" @click="clickAddOrEditConfirm">确认</el-button>
            </template>
        </el-card>
        <!-- 表格主体 -->
        <el-card style="margin: 10px 0" v-show="currentShowType==='table'">
            <el-button type="primary" :icon="Plus" @click="openAddDialog" :disabled="!spuList.length" v-btnPermission="'添加SPU'">添加SPU</el-button>
            <!-- 表格 -->
            <el-table style="margin: 10px 0" border :data="showSpuList" class="table" stripe>
                <el-table-column label="序号" prop="序号" width="150" align="center"></el-table-column>
                <el-table-column label="SPU名称" prop="SPU名称" width="300" align="center">
                </el-table-column>
                <el-table-column label="SPU描述" prop="SPU描述" width="900" align="center">
                    <template #="{ row }">
                        <p>&emsp;&emsp;{{ row.SPU描述 }}</p>
                    </template>
                </el-table-column>
                <el-table-column label="SPU操作" width="400" align="center" fixed="right">
                    <template #="{ row, $index }">
                        <el-button type="success" :icon="Edit" @click="openEditDialog(row.序号, $index)" v-btnPermission="'修改SPU'"></el-button>
                        <el-popconfirm title="确定删除该spu信息？" @confirm="deleteOneSpu(row.序号)">
                            <template #reference>
                                <el-button type="danger" v-btnPermission="'删除SPU'">
                                    <el-icon>
                                        <Delete />
                                    </el-icon>
                                </el-button>
                            </template>
                        </el-popconfirm>
                        <el-button type="primary" :icon="Plus" @click="addSku(row.序号)" v-btnPermission="'添加SKU'">SKU</el-button>
                        <el-button type="warning" :icon="View" @click="viewSku(row.序号)" v-btnPermission="'查看SKU'">SKU</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
        <SkuDialog v-model:isSkuDialogShow="isSkuDialogShow" v-model:currentSelectedNum="currentSelectedNum" v-model:isSkuAddOrViewOrEdit="isSkuAddOrViewOrEdit"></SkuDialog>
        <!-- 分页器 -->
        <div class="pagination" v-show="currentShowType==='table'">
            <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" :page-sizes="[3, 5, 7]"
                :background="true" layout="sizes, prev, pager, next, total, jumper" :total="total"
                @size-change="pageSizeChange" @current-change="pageNoChange" :hide-on-single-page="true" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, computed, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import useProductSpuStore from '@/stores/product/spu'
import SpuCategory from './SpuCategory/index.vue'
import { Plus, Edit, Delete, Goods,View } from '@element-plus/icons-vue'
import { ElMessage, type UploadFile } from 'element-plus'

defineOptions({ name: 'Spu' });
let { pageNo, pageSize, total, spuList, start, oneSpuDetailInfo } = storeToRefs(useProductSpuStore());
let { changePage, deleteOneSpu, addOneSpu, getOneSpuDetail, clearOneSpuDetail, editOneSpu, reset } = useProductSpuStore();

// SKU部分动画是否显示
let isSkuDialogShow = ref(false);
// 点了添加还是查看
let isSkuAddOrViewOrEdit = ref('');
// 传当前点添加或预览sku的序号，三级分类不传，可以从仓库获取
const addSku = (num: number)=>{
    isSkuDialogShow.value= true;
    currentSelectedNum.value = num;
    isSkuAddOrViewOrEdit.value = 'add';
};
const viewSku = (num: number)=>{
    isSkuDialogShow.value= true;
    currentSelectedNum.value = num;
    isSkuAddOrViewOrEdit.value = 'view';
};

// 展示的本页spuList，需要加工一下
let showSpuList = computed(() => {
    let tmp: any = [];
    spuList.value.forEach((item: any, index: number) => {
        tmp.push({
            '序号': start.value + index,
            'SPU名称': item.spuName,
            'SPU描述': item.description,
        });
    })
    return tmp
});
// 切换每页属性显示数量
const pageSizeChange = async (value: number) => {
    await changePage(pageNo.value, value);
};
// 切换页码
const pageNoChange = async (value: number) => {
    await changePage(value, pageSize.value);
};

// 是添加还是编辑
let isAddOrEdit = ref('');
// 添加、编辑弹窗是否显示
let currentShowType = ref('table');
// 添加的PSU名称
let addSpuName = ref('');
// 添加的SPU描述
let addSpuDescription = ref('');
// 上传图片的上传组件实例
let uploadImage = ref();
// 上传的图片名字数组
let uploadImageNameList: any = ref([]);
// 上传的图片链接数组
let uploadImageUrlList: any = ref([]);
// 图片名和链接组合在一起，用于显示图片
let uploadImageNameAndUrlList: any = ref([]);
// 目前要显示大图的图片链接
let currentImageUrl = ref(''); // 要上传
// 预览图是否显示
let isPreviewDialogShow = ref(false);
// 添加的SPU数组
let addSpuPropsList = ref<any>([]);
// 添加的SPU的单个标签接口
interface addSpuOneTagType {
    '序号': number
    '属性': string
    '标签': string[]
    '标签颜色': string[]
};
// 输入框实例
let input = ref();
// 添加的SPU属性输入框内容
let addPropInputContent: any = ref([]);
// 添加标签时的输入框是否显示
let isAddTagInputShow: any = ref([]);
// 该输入框的内容
let addTagInputContent: any = ref([]);
// 添加时选中的颜色是哪个
let addTagColor: any = ref([]);
// 当前编辑的序号，编辑时用到
let currentSelectedNum = ref(0);

// 初始化空白切换组件
const initDialog = () => {
    addSpuDescription.value = '';
    uploadImageNameList.value = [];
    uploadImageUrlList.value = [];
    addSpuPropsList.value = [];
    addPropInputContent.value = [];
    isAddTagInputShow.value = [];
    addTagInputContent.value = [];
    addTagColor.value = [];
    uploadImageNameAndUrlList.value = [];
}
// 打开添加切换组件
const openAddDialog = () => {
    clearOneSpuDetail(); // 先清空原来的
    isAddOrEdit.value = '添加SPU';
    currentShowType.value = 'addOrEdit';
    addSpuName.value = '';
    // try {
    //     uploadImage.value.clearFiles(); // 清空之前已上传的文件
    // } catch (e) { }
};
// 选了图片，把链接加到数组中
const uploadStateChange = (file: UploadFile) => {
    uploadImageUrlList.value.push(file.url!);
    uploadImageNameList.value.push(file.name);
    uploadImageNameAndUrlList.value.push({ name: file.name, url: file.url! });
};
// 点击展示预览图
const handlePictureCardPreview = (file: UploadFile) => {
    currentImageUrl.value = file.url!;
    isPreviewDialogShow.value = true;
};
// 点击删除某个图
const handleRemove = (file: UploadFile) => {
    // 数组中删掉对应的链接
    uploadImageUrlList.value = uploadImageUrlList.value.filter((item: string) => item !== file.url);
    uploadImageNameList.value = uploadImageNameList.value.filter((item: string) => item !== file.name);
    uploadImageNameAndUrlList.value = uploadImageNameAndUrlList.value.filter((item: any) => item.name !== file.name);
};
// 添加一个属性
const addOneSpuProp = () => {
    addSpuPropsList.value.push({
        '序号': addSpuPropsList.value.length + 1,
        '属性': '',
        '标签': [],
        '标签颜色': []
    });
    addPropInputContent.value.push('');
    isAddTagInputShow.value.push(false);
    addTagInputContent.value.push('');
    addTagColor.value.push(0);
};
// 删除一个属性
const deleteOneSpuTag = (num: number) => {
    addSpuPropsList.value.splice(num - 1, 1);
    // 序号重排
    addSpuPropsList.value = addSpuPropsList.value.map((item: addSpuOneTagType, index: any) => {
        item.序号 = index + 1;
        return item
    });
    addPropInputContent.value.splice(num - 1, 1);
    isAddTagInputShow.value.splice(num - 1, 1);
    addTagInputContent.value.splice(num - 1, 1);
    addTagColor.value.splice(num - 1, 1);
};
// 属性输入完成，输入框失焦
const addPropInputBlur = (num: number) => {
    // 过滤掉空的、还没输入的属性，留到最后提交时再检测
    let removeEmpty = addPropInputContent.value.filter((item: string) => item);
    let set = new Set(removeEmpty);
    if (set.size !== removeEmpty.length) {
        ElMessage({
            type: 'warning',
            message: '属性不能重复'
        });
        addPropInputContent.value[num - 1] = '';
        return
    }
    addSpuPropsList.value[num - 1].属性 = addPropInputContent.value[num - 1];
};
// 给某个属性添加一个标签时的颜色
let reflection = ['primary', 'success', 'info', 'warning', 'danger'];
// 给某个属性添加一个标签，显示输入框并保存选的颜色
const showInputAndSendColor = async (num: number, color: number) => {
    isAddTagInputShow.value[num - 1] = true;
    addTagColor.value[num - 1] = color;
    await nextTick();
    input.value.focus(); // 自动获得焦点
};
// 标签输入完成，输入框失焦
const addTagInputBlur = (num: number) => {
    // num: 序号
    // 如果啥也没输入
    if (!addTagInputContent.value[num - 1]) return
    // 如果标签重复
    if (addSpuPropsList.value[num - 1].标签.includes(addTagInputContent.value[num - 1])) {
        ElMessage({
            type: 'warning',
            message: '同一属性的标签不能重复'
        });
        addTagInputContent.value[num - 1] = '';
        input.value.focus();
        return
    }
    addSpuPropsList.value[num - 1].标签.push(addTagInputContent.value[num - 1]);
    addSpuPropsList.value[num - 1].标签颜色.push(addTagColor.value[num - 1]);
    // 置空，防止再在这个标签上加标签时显示原来的
    addTagInputContent.value[num - 1] = '';
    // addTagColor.value[num - 1] = 0; // 颜色不用改
    // 最后才不显示输入框
    isAddTagInputShow.value[num - 1] = false;
}
// 删除某个属性的某个标签
const removeOneTag = (num: number, index: number) => {
    // 序号，标签索引
    addSpuPropsList.value[num - 1].标签.splice(index, 1);
    addSpuPropsList.value[num - 1].标签颜色.splice(index, 1);
};
// 切换组件取消
const cancelAndSendReq = ()=>{
    currentShowType.value = 'table';
    initDialog();
}
// 切换组件确认
let timer: any; // 计时器，节流
// 判断并发送请求函数
const confirmAndSendReq = async () => {
    if (!addSpuName.value) { ElMessage({ type: 'warning', message: 'SPU名称不能为空' }); return }
    if (!addSpuDescription.value) { ElMessage({ type: 'warning', message: 'SPU描述不能为空' }); return }
    if (uploadImageUrlList.value.length === 0) { ElMessage({ type: 'warning', message: '至少上传一张SPU图片' }); return }
    if (addSpuPropsList.value.length === 0) { ElMessage({ type: 'warning', message: '至少添加一个属性' }); return }
    let sign = 0;
    addSpuPropsList.value.forEach((item: addSpuOneTagType, index: number) => {
        if (item.属性 === '') { ElMessage({ type: 'warning', message: `属性值不能为空，请检查第${index + 1}个属性` }); sign = 1; return }
        if (item.标签.length === 0) { ElMessage({ type: 'warning', message: `每个属性至少添加一个标签，请检查第${index + 1}个属性` }); sign = 1; return }
    });
    if (sign) { return }
    let formData = new FormData();
    formData.append('spuName', addSpuName.value);
    formData.append('spuDescription', addSpuDescription.value);
    formData.append('spuPropsList', JSON.stringify(addSpuPropsList.value));
    // 处理图片
    let originalImageNameList = []; // 原来的图片，不做处理，返回图片名
    for (let i = 0; i < uploadImageUrlList.value.length; i++) {
        if (uploadImageUrlList.value[i].includes('?timestamp')) {
            let imageName = uploadImageUrlList.value[i].split('?timestamp')[0].split('spu/')[1];
            originalImageNameList.push(imageName);
            // 需要把原来有的图片移除
        } else {
            let url = uploadImageUrlList.value[i];
            let result = await fetch(url);
            const r = await result.blob();
            formData.append(`images`, r, uploadImageNameList.value[i]);
        }
    }
    formData.append('originalImageNameList', JSON.stringify(originalImageNameList));
    // 不能用forEach执行异步，不然append不进去
    // uploadImageUrlList.value.forEach(async (item: string, index: number) => {
    //     const result = await fetch(item);
    //     const r = await result.blob();
    //     formData.append(`images`, r, uploadImageNameList.value[index]);
    // });
    if (isAddOrEdit.value === '添加SPU') {
        await addOneSpu(formData);
    } else {
        formData.append('num', currentSelectedNum.value.toString());
        await editOneSpu(formData);
    }
    currentShowType.value = 'table';
    initDialog();
}
const clickAddOrEditConfirm = async () => {
    if (timer) { return }
    timer = setTimeout(() => {
        timer = null;
    }, 3000);
    await confirmAndSendReq();
};
// 打开编辑切换组件
const openEditDialog = async (num: number, $index: number) => {
    currentSelectedNum.value = num;
    clearOneSpuDetail(); // 先清空原来的
    await getOneSpuDetail(num);
    isAddOrEdit.value = '编辑SPU';
    currentShowType.value = 'addOrEdit';
    addSpuName.value = showSpuList.value[$index].SPU名称;
    addSpuDescription.value = showSpuList.value[$index].SPU描述;
    uploadImageNameList.value = oneSpuDetailInfo.value.images.map((item: string) => item.split('spu/')[1].split('?')[0]);
    uploadImageUrlList.value = oneSpuDetailInfo.value.images;
    addSpuPropsList.value = oneSpuDetailInfo.value.props;
    addPropInputContent.value = oneSpuDetailInfo.value.props.map((item: any) => item.属性);
    isAddTagInputShow.value = [];
    addTagInputContent.value = [];
    addTagColor.value = [];
    uploadImageNameAndUrlList.value = uploadImageNameList.value.map((item: any, index: number) => {
        return {
            name: item,
            url: uploadImageUrlList.value[index]
        }
    });
};

onBeforeUnmount(() => {
    reset();
});


</script>

<style scoped lang="scss">
.table {
    text-align: center;
}

.oneTag {
    margin: 5px;
}

.addOneTagPlus {
    margin-left: 30px;
    border: none;
    font-size: 20px;
}

.addOneTagInput {
    width: 70px;
    height: 25px;
}

.pagination {
    transform: translateX(30%);
}
</style>