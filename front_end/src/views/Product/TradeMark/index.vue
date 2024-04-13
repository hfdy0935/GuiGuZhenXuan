<template>
    <el-card class="box-card">
        <el-button type="primary" icon="plus" size="default" @click="clickAddTradeMark" v-btnPermission="'添加品牌'">添加品牌</el-button>
        <!-- 添加和修改品牌信息的对话框 -->
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500">
            <el-form label-position="right">
                <el-card>
                    <el-form-item label="名称：" label-width="90px">
                        <el-input type="text" v-model="logoName" placeholder="品牌名称"></el-input>
                    </el-form-item>
                    <el-form-item label="LOGO：" label-width="90px">
                        <el-upload class="avatar-uploader" :action="`/api/user/profilePicture/success/${Date.now()}`"
                            :show-file-list="false" :headers="{ token }" :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload">
                            <img v-if="logoUrl" :src="logoUrl" class="avatar" />
                            <el-icon v-else class="avatar-uploader-icon">
                                <Plus />
                            </el-icon>
                        </el-upload>
                    </el-form-item>
                </el-card>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="confirm">确认</el-button>
                </div>
            </template>
        </el-dialog>
        <!-- 表格组件 -->
        <el-table :data="currentTradeMarkList" style="width: 100%; margin: 10px 0;" border>
            <el-table-column label="序号" width="100" align="center">
                <template #="{ row }">
                    <h1 style="font-size: 20px;">{{ row.index }}</h1>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="品牌名称" width="180" align="center" />
            <el-table-column label="品牌LOGO" width="200" align="center">
                <template #="{ row}">
                    <div class="demo-image__preview">
                        <img :src="row.logo" width="120px"/>
                        <!-- <el-image style="height: 80px" :title="row.name" :alt="row.name" :src="row.logo" :zoom-rate="1.2"
                            :max-scale="3.5" :min-scale="0.6" :preview-src-list="currentPicList" :initial-index="$index"
                            fit="cover" /> -->
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
                <template #="{ row }">
                    <el-button type="primary" :icon="Edit" round v-btnPermission="'修改品牌'"
                        @click="clickUpdateTradeMark(row.index, row.logo, row.name)"></el-button>
                    <el-button type="danger" :icon="Delete" round @click="clickDeleteTradeMark(row.index)" v-btnPermission="'删除品牌'"></el-button>
                </template>
            </el-table-column>
        </el-table>
        <!-- 分页器 -->
        <div class="pagination">
            <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" :page-sizes="[3, 5, 10]"
                :background="true" layout="sizes, prev, pager, next, total, jumper" :total="totalNum"
                @size-change="reqCurrentPageTradeMarkList" @current-change="reqCurrentPageTradeMarkList" />
        </div>
    </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, markRaw } from 'vue'
import { storeToRefs } from 'pinia'
import { reqTradeMark } from '@/api/product/trademark'
import { Edit, Delete } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { reqAddTradeMark, reqUpdateTradeMark, reqDeleteTradeMark } from '@/api/product/trademark'
import useProductTradeMarkStore from '@/stores/product/trademark'
import useUserStore from '@/stores/user'

defineOptions({ name: 'TradeMark' });

let { token } = storeToRefs(useUserStore());
let { pageNo, pageSize } = storeToRefs(useProductTradeMarkStore());
let { changeCurrentPage, changePageSize } = useProductTradeMarkStore();
let totalNum = ref(0);
// 本页品牌列表
let currentTradeMarkList: any = reactive([]);
// LOGO链接列表
// let currentPicList: any = ref([]);

// 根据当前每页要现实的数量和本业页数发送请求
async function reqCurrentPageTradeMarkList() {
    let result: any = await reqTradeMark({
        pageNo: pageNo.value,
        pageSize: pageSize.value
    });
    if (result.code === 200) {
        Object.keys(currentTradeMarkList).forEach((item: any) => {
            delete currentTradeMarkList[item];
        })
        changeCurrentPage(pageNo.value);
        changePageSize(pageSize.value);
        Object.assign(currentTradeMarkList, result.data.tradeMarkList);
        // currentPicList.value = currentTradeMarkList.map((item: any) => item.logo)
        totalNum.value = result.data.totalNum;

    }
}
onMounted(async () => {
    reqCurrentPageTradeMarkList();
});

// 添加、修改品牌
let dialogVisible = ref<boolean>(false); // 对话框是否可见
let dialogTitle = ref<string>(''); // 对话框标题
let logoName = ref(''); // logo人为命名
let logoUrl = ref(''); // logo临时二进制链接
let filename = ref(''); // logo文件名
let selectedIndex = ref(0); // 点编辑或删除的品牌序号，从1开始
// 清空原来的logo名和图
const clearOriginalLogo = () => {
    logoName.value = '';
    logoUrl.value = '';
}

// 上传logo成功，还没点确认
const handleAvatarSuccess: UploadProps['onSuccess'] = (
    _,
    uploadFile
) => {
    filename.value = uploadFile.name;
    logoUrl.value = URL.createObjectURL(uploadFile.raw!);
};
// 文件上传前的检查
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    if (!['image/jpeg', 'image/png', 'image/gif', 'image/avif'].includes(rawFile.type)) {
        ElMessage.error('只支持jpg、png、gif、avif格式!')
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('文件最大2MB！')
        return false
    }
    return true
}
// 点添加品牌
function clickAddTradeMark() {
    clearOriginalLogo();
    dialogVisible.value = true;
    dialogTitle.value = '添加品牌信息';
}
// 点编辑品牌，index序号
function clickUpdateTradeMark(index: number, logo: string, name: string) {
    clearOriginalLogo();
    dialogVisible.value = true;
    dialogTitle.value = '修改品牌信息';
    selectedIndex.value = index;
    logoUrl.value = logo;
    logoName.value = name;
}
// 点确认
async function confirm() {
    if (logoName.value === '') {
        ElMessage({
            type: 'error',
            message: '品牌名不能为空'
        });
        return
    }
    if (logoUrl.value === '') {
        ElMessage({
            type: 'error',
            message: '品牌logo不能为空'
        });
        return
    }
    dialogVisible.value = false;
    let formData: any = new FormData();
    // 修改和追加logo的情况
    if (logoUrl.value.includes('blob')) {
        let r = await fetch(logoUrl.value);
        let rr = await r.blob();
        formData.append('logo', rr, filename.value);
    }
    // 增加、修改都有
    formData.append('name', logoName.value);
    let result: any = '';
    // 传了索引，要修改
    if (dialogTitle.value === '修改品牌信息') {
        formData.append('index', selectedIndex.value);
        result = await reqUpdateTradeMark(formData);
    } else {
        result = await reqAddTradeMark(formData);
    }
    if (result.code === 200) {
        // 更新页面
        await reqCurrentPageTradeMarkList();
        ElMessage({
            type: 'success',
            message: result.msg
        });
    }
}
// 删除一个品牌，index先从1开始
async function clickDeleteTradeMark(index: number) {
    let result: any;
    try {
        await ElMessageBox.confirm(
            '确认要删除所选品牌吗？',
            {
                type: 'warning',
                icon: markRaw(Delete),
            }
        )
        result = await reqDeleteTradeMark({ index });
        if (result.code === 200) {
            // 更新页面
            await reqCurrentPageTradeMarkList();
        }
    } catch (e) { }
}


</script>

<style scoped lang="scss">
.pagination {
    display: flex;
    justify-content: center;

}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}

.avatar-uploader .avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>@/api/product/trademark