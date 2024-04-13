<template>
    <div class="container">
        <AttrCategory></AttrCategory>
        <div class="card2">
            <el-card>
                <!-- 添加属性按钮 -->
                <el-button type="primary" icon="Plus" class="addOneAttrBtn" @click="openAddDialog"  :disabled="!attrList.length" v-btnPermission="'添加属性'">添加平台属性</el-button>
                <!-- 添加、编辑对话框 -->
                <el-dialog v-model="isDialogShow" :title="isAddOrEdit" width="600px">
                    <!-- 添加/编辑属性对话框表格 -->
                    <el-form class="form" label-position="right">
                        <el-form-item label="属性名" class="nameItem">
                            <el-input v-model="addAttrName"></el-input>
                        </el-form-item>
                        <!-- 每条属性 -->
                        <div class="addAttrValue" v-for="(_, propIndex) in addAttrNum" :key="propIndex">
                            <el-form-item :label="`属性值${propIndex + 1}`" class="infoItem">
                                <el-input v-model="addAttrInfo[propIndex]"></el-input>
                            </el-form-item>
                            <el-form-item label="颜色">
                                <el-button v-for="(item, index) in reflection" :key="index" :type="item" :label="item"
                                    :icon="addAttrColor[propIndex] === item ? Select : ''"
                                    @click="addAttrColor[propIndex] = item"></el-button>
                            </el-form-item>&emsp;
                            <Close class="deleteOneAttrIcon" @click="deleteOneAttrInAdd(propIndex)"
                                v-if="addAttrNum !== 1" />
                        </div>
                        <el-button type="success" :icon="Plus" @click="addOneAttrValue">新建属性</el-button>
                    </el-form>
                    <template #footer>
                        <el-button @click="isDialogShow = false">取消</el-button>
                        <el-button type="primary" @click="checkAddOneAttr">确认</el-button>
                    </template>
                </el-dialog>
                <!-- 表格 -->
                <el-table border class="table" stripe :data="showAttrListData">
                    <el-table-column label="序号" prop='序号' align="center">
                    </el-table-column>
                    <el-table-column label="属性名称" prop='属性名称' align="center">
                        <template v-slot="{ row }">
                            <el-icon>
                                <component :is="row.序号%2==0? Apple: IceTea"></component>
                            </el-icon>
                            {{ row.属性名称 }}
                        </template>
                    </el-table-column>
                    <el-table-column label="属性值" prop='属性值' align="center" width="600">
                        <template v-slot="{ row }">
                            <el-tag v-for="(item, index) in row.属性值" :key="index" class="tag"
                                :type="reflection[parseInt(item[item.length - 1])]">
                                {{ item.slice(0, item.length - 1) }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" type="index" width="300" fixed="right" align="center">
                        <template v-slot="{ row }">
                            <el-button type="primary" @click="openEditDialog(row)" v-btnPermission="'修改属性'"><el-icon>
                                    <Edit />
                                </el-icon>编辑</el-button>
                            <el-popconfirm title="确定删除该属性？" @confirm="deleteOneAttr(row.序号)">
                                <template #reference>
                                    <el-button type="danger" v-btnPermission="'删除属性'">
                                        <el-icon>
                                            <Delete />
                                        </el-icon>删除
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
                <br />
                <!-- 分页器 -->
                <div class="pagination">
                    <el-pagination v-model:current-page="pageNo" v-model:page-size="pageSize" :page-sizes="[3, 5, 7]"
                        :background="true" layout="sizes, prev, pager, next, total, jumper" :total="total"
                        @size-change="pageSizeChange" @current-change="pageNoChange" :hide-on-single-page="true" />
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'
import useProductAttrStore from '@/stores/product/attr'
import { Apple, IceTea, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { Select, Plus } from '@element-plus/icons-vue'
import AttrCategory from './AttrCategory/index.vue'

defineOptions({ name: 'Attr' });

let { pageNo, pageSize, total, attrList, start } = storeToRefs(useProductAttrStore());
let { changePage, deleteOneAttr, addOneAttr, editOneAttr, reset } = useProductAttrStore();

// 在表格中显示的数据
let showAttrListData = computed(() => {
    let tmp: any = [];
    attrList.value.forEach((item: any, index: number) => {
        tmp.push({
            '序号': start.value + index,
            '属性名称': Object.keys(item)[0],
            '属性值': Object.values(item)[0]
        });
    });
    return tmp
});
// 不同属性标签对应关系
let reflection = ['primary', 'success', 'info', 'warning', 'danger'];


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
// 添加属性、编辑属性弹窗
let isDialogShow = ref(false);
// 添加的属性名
let addAttrName = ref('');
// 添加的属性值和颜色
let addAttrInfo = ref([]);
let addAttrColor = ref<string[]>([]);
// 属性数量
let addAttrNum = ref(1);
// 打开添加对话框
const openAddDialog = () => {
    isAddOrEdit.value = '添加属性';
    // 清空之前填写的东西
    addAttrName.value = '';
    addAttrInfo.value = [];
    addAttrColor.value = ['primary'];
    addAttrNum.value = 1;
    isDialogShow.value = true;
}
// 打开编辑对话框
let editingNum = ref(0); // 储存点了编辑的那个属性的序号
const openEditDialog = (item: any) => {
    isAddOrEdit.value = '编辑属性';
    addAttrName.value = item.属性名称;
    // 去掉最后的数字
    addAttrInfo.value = item.属性值.map((i: any) => i.slice(0, i.length - 1));
    addAttrColor.value = item.属性值.map((i: any) => reflection[i.slice(i.length - 1)]);
    addAttrNum.value = item.属性值.length;
    isDialogShow.value = true;
    editingNum.value = item.序号;
}
// 新建属性值
const addOneAttrValue = () => {
    addAttrNum.value += 1;
    addAttrColor.value.push('primary');
};
// 点添加属性中每个属性后面的×删除该属性
const deleteOneAttrInAdd = (index: number) => {
    addAttrInfo.value.splice(index, 1);
    addAttrColor.value.splice(index, 1);
    addAttrNum.value -= 1;
}
// 对话框点确认之后检查，没问题再提交
const checkAddOneAttr = async () => {
    if (!addAttrName.value) {
        ElMessage({
            type: 'error',
            message: '属性名不能为空'
        });
        return
    }
    if (addAttrInfo.value.length !== addAttrNum.value) {
        ElMessage({
            type: 'error',
            message: '属性值不能为空'
        });
        return
    }
    let set = new Set(addAttrInfo.value);
    if (set.size < addAttrInfo.value.length) {
        ElMessage({
            type: 'warning',
            message: '属性值不能重复'
        });
        return
    }
    isDialogShow.value = false;
    let tmp: any = [];
    // 转为后端储存的格式
    addAttrColor.value.forEach((item, index) => {
        tmp[index] = addAttrInfo.value[index] + reflection.indexOf(item);
    });
    if (isAddOrEdit.value === '添加属性') {
        await addOneAttr({
            name: addAttrName.value,
            'value': tmp
        });
    } else {
        await editOneAttr({
            name: addAttrName.value,
            'value': tmp,
            'index': editingNum.value
        });
    }

};
onBeforeUnmount(() => {
    reset();
});



</script>

<style scoped lang="scss">
.container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: space-evenly;

    .card2 {
        width: 100%;
        height: 80%;
        box-shadow: 0 0 5px orange;

        .addOneAttrBtn {
            margin-bottom: 20px;
        }

        .form {
            width: 500px;
            text-align: center;

            .nameItem {
                width: 180px;
            }


            .addAttrValue {
                display: flex;

                .infoItem {
                    width: 180px;
                    margin-right: 30px;
                }

                .deleteOneAttrIcon {
                    width: 12px;
                    position: relative;
                    top: -6px;

                    &:hover {
                        color: red;
                    }
                }
            }
        }


        .table {
            overflow: auto;

            .tag {
                margin-right: 5px;
                margin-bottom: 10px;
            }
        }

        .pagination {
            transform: translateX(30%);
        }

    }
}
</style>