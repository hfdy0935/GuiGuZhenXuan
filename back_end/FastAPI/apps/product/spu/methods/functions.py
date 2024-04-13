import numpy as np
import json
import os
import aiofiles
import random


async def get_spu_list_main(c1id: int):
    '''
    获取对应一级分类json中的属性
    '''
    c1_list = os.listdir('./data/product/spu/spuListData')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/spuListData/{c1_name}', 'r', encoding='utf-8') as f:
        spu_list = json.loads(await f.read())
        return spu_list


async def get_sku_before_add_list_main(c1id: int):
    '''
    获取一级分类下，添加sku之前的选项
    '''
    c1_list = os.listdir('./data/product/spu/skuInSpuBeforeAdd')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/skuInSpuBeforeAdd/{c1_name}', 'r', encoding='utf-8') as f:
        sku_list = json.loads(await f.read())
        return sku_list

async def get_sku_list_main(c1id: int):
    '''
    获取正式的sku列表
    '''
    c1_list = os.listdir('./data/product/spu/addSkuList')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/addSkuList/{c1_name}', 'r', encoding='utf-8') as f:
        sku_list = json.loads(await f.read())
        return sku_list

async def set_spu_list_main(c1id, value: dict):
    '''
    修改对应一级分类json中的属性
    '''
    c1_list = os.listdir('./data/product/spu/spuListData')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/spuListData/{c1_name}', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def set_sku_before_add_list_main(c1id: int, value: dict):
    '''
    增改查
    '''
    c1_list = os.listdir('./data/product/spu/skuInSpuBeforeAdd')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/skuInSpuBeforeAdd/{c1_name}', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)

async def set_sku_list_main(c1id: int, value: dict):
    '''
    写入
    '''
    c1_list = os.listdir('./data/product/spu/addSkuList')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/addSkuList/{c1_name}', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)
    
    
def generate_sku_before_add_info():
    '''
    新增一个spu时要添加对应的sku选项
    '''
    # 生成spu中的sku部分数据
    name = ['华为', 'VIVO', 'OPPO', '三星', '小米', '山寨', '魅族', '苹果',
            '诺基亚', '中兴', '金立', '酷派', 'HTC', 'LG', '夏普', '台电', '天语']
    price = [int(i)+99 for i in np.arange(1500, 25000, 100)]
    weight = [int(i) for i in np.arange(400, 1000, 5)]
    description = [i+'手机，至尊选择' for i in name]
    # 平台属性
    mobile = name
    battery = [str(i)+'mAh' for i in np.arange(800, 3000, 50)]
    runMemory = ['128MB', '256MB', '512MB', '1GB', '2GB', '3GB', '4GB',
                 '8GB', '16GB', '32GB', '64GB', '128GB', '256GB', '512GB', '1TB']
    selfMemory = ['128MB', '256MB', '512MB', '1GB', '2GB', '3GB', '4GB', '8GB', '16GB',
                  '32GB', '64GB', '128GB', '256GB', '512GB', '1TB', '2TB', '4TB', '8TB', '16TB']
    cpuType = ['ARM', 'x86', 'MIPS', 'RISC-V', 'x86_64', 'MIPS64']
    screenSize = ['1280*720', '1920*1080',
                  '2560*1440', '3840*2160', '4096*2160']
    # 售卖属性
    color = ['红色', '绿色', '蓝色', '黄色', '紫色', '粉色', '灰色', '白色', '黑色', '橙色']
    version = ['1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '3.0', '3.1',
               '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '4.0', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '5.0', '5.1', '5.2', '5.3', '5.4']

    props = {
        'platformProps': {
            'mobile': random.sample(mobile, random.randint(3, 9)),
            'battery': random.sample(battery, random.randint(3, 8)),
            'runMemory': random.sample(runMemory, random.randint(3, 10)),
            'selfMemory': random.sample(selfMemory, random.randint(3, 7)),
            'cpuType': random.sample(cpuType, random.randint(2, 5)),
            'screenSize': random.sample(screenSize, random.randint(2, 5))
        },
        'saleProps': {
            'color': random.sample(color, random.randint(3, 8)),
            'version': random.sample(version, random.randint(8, 9))
        }
    }
    return props


############
async def get_spu_list(c1id: int, c2id: int, c3id: int, pageNo: int, pageSize: int):
    '''
    获取spu列表
    '''
    spu_list = await get_spu_list_main(c1id)
    data = list(spu_list['contents'][c2id - 1][c3id].values())[0]
    [i.pop('images') for i in data]  # 目前图片和具体属性不用发
    [i.pop('props') for i in data]
    start = (pageNo - 1) * pageSize
    end = start + pageSize  # 左闭右开
    return {
        'data': data[start:end],
        'total': len(data),
        'pageNo': pageNo,
        'pageSize': pageSize,
        'start': start + 1,
        'end': end
    }


async def delete_one_spu(c1id: int, c2id: int, c3id: int, index: int):
    '''
    根据索引删除某个spu
    从1开始
    '''
    try:
        spu_list = await get_spu_list_main(c1id)
        c3name = list(spu_list['contents'][c2id - 1][c3id].keys())[0]
        data = list(spu_list['contents'][c2id - 1][c3id].values())[0]
        del data[index-1]
        spu_list['contents'][c2id - 1][c3id][c3name] = data
        await set_spu_list_main(c1id, spu_list)

        # 删除该spu对应的sku添加前属性
        sku_before_add = await get_sku_before_add_list_main(c1id)
        data = list(sku_before_add['contents'][c2id - 1][c3id].values())[0]
        del data[index-1]
        sku_before_add['contents'][c2id - 1][c3id][c3name] = data
        await set_sku_before_add_list_main(c1id, sku_before_add)

        # spu都没了sku也得删，防止序号出现错误
        sku_list = await get_sku_list_main(c1id)
        del sku_list['contents'][c2id - 1][c3id][c3name][index-1]
        await set_sku_list_main(c1id, sku_list)
            
        return True
    except:
        return False


async def add_one_spu(spuName, spuDescription, spuPropsList, c1id, c2id, c3id, image_url_list) -> bool:
    '''
    添加一个spu
    '''
    try:
        spu_list = await get_spu_list_main(c1id)
        target_dict = {
            'spuName': spuName,
            'description': spuDescription,
            'images': image_url_list,
            'props': eval(spuPropsList)
        }
        c3name = list(spu_list['contents'][c2id - 1][c3id].keys())[0]
        spu_list['contents'][c2id - 1][c3id][c3name].append(target_dict)
        await set_spu_list_main(c1id, spu_list)

        # 添加该spu对应的sku添加前属性
        sku_before_add = await get_sku_before_add_list_main(c1id)
        dic: dict = generate_sku_before_add_info()
        dic['images'] = image_url_list #图片
        t = [0]*len(image_url_list) # 默认选择
        t[random.randint(0, len(t))] = 1
        dic['isDefault'] = t
        sku_before_add['contents'][c2id - 1][c3id][c3name].append(dic)
        await set_sku_before_add_list_main(c1id, sku_before_add)
        
        # 还得给该spu的sku列表新建一项
        sku_list = await get_sku_list_main(c1id)
        tmp = sku_list['contents'][c2id - 1][c3id][c3name]
        sku_list['contents'][c2id - 1][c3id][c3name].append({
            '序号': len(tmp)+1,
            'spuName': spuName,
            'skuInfo': []
        })
        await set_sku_list_main(c1id, sku_list)

        return True
    except:
        return False


async def get_spu_detail(c1id: int, c2id: int, c3id: int, num: int):
    '''
    获取某个spu详情
    '''
    try:
        spu_list = await get_spu_list_main(c1id)
        data = list(spu_list['contents'][c2id - 1][c3id].values())[0]
        [i.pop('spuName') for i in data]  # 只发送spu名和描述
        [i.pop('description') for i in data]
        return data[num-1]
    except:
        return False


async def edit_one_spu(spuName: str, spuDescription: str, spuPropsList: str, c1id: int, c2id: int, c3id: int, num: int, image_url_list: list[str]):
    '''
    编辑某个spu
    '''
    try:
        spu_list = await get_spu_list_main(c1id)
        target_dict = {
            'spuName': spuName,
            'description': spuDescription,
            'images': image_url_list,
            'props': eval(spuPropsList)
        }
        # 替换
        c3name = list(spu_list['contents'][c2id - 1][c3id].keys())[0]
        spu_list['contents'][c2id - 1][c3id][c3name][num-1] = target_dict
        await set_spu_list_main(c1id, spu_list)

        # 编辑该spu对应的sku添加前属性
        sku_before_add = await get_sku_before_add_list_main(c1id)
        sku_before_add['contents'][c2id -
                                   1][c3id][c3name][num-1]['images'] = image_url_list
        await set_sku_before_add_list_main(c1id, sku_before_add)

        
        return True
    except:
        return False
