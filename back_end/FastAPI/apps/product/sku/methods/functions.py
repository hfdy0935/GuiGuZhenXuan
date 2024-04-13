import json
import aiofiles
import os
import random
import time
from ..methods.types import Item

path = './data/product/spu/addSkuList'
json_list = os.listdir(path)
path_list = [os.path.join(path, i) for i in json_list]


def get_random_five_images():
    images_list = random.sample(os.listdir('./static/spu'), 5)
    url_list = [
        f'/api/static/spu/{i}?timestamp={time.time()}' for i in images_list
    ]
    return url_list


def parse_one_json(data: dict, c1id: int):
    '''
    解析一个json，提取出skuInfo
    '''
    result = []
    for c2id, c2 in enumerate(data['contents'], start=1):
        for c3id, c3 in enumerate(c2[1:], start=1):
            value = list(c3.values())[0]
            r = []
            num = []
            for index, i in enumerate(value, start=1):
                if i['skuInfo']:
                    r.append(i['skuInfo'])
                    num.append(index)
            if r:
                for index, j in enumerate(r):
                    for index1, k in enumerate(j, start=1):
                        k['c1id'] = c1id
                        k['c2id'] = c2id
                        k['c3id'] = c3id
                        k['c3num'] = num[index]  # 三级分类下商品的序号，从1开始
                        k['skuNum'] = index1  # 该序号的商品下的sku的序号
                        k['detailImages'] = get_random_five_images()
                        result.append(k)
    return result


async def get_c1_sku(c1id: int):
    '''
    根据c1id返回对应的.json内容
    '''
    filename = [i for i in json_list if int(i.split('_')[0]) == c1id][0]
    filepath = os.path.join(path, filename)
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
        data = await f.read()
        data = json.loads(data)
        return data


async def set_c1_sku(c1id: int, data: dict):
    '''
    修改c1分类下的sku
    '''
    filename = [i for i in json_list if int(i.split('_')[0]) == c1id][0]
    filepath = os.path.join(path, filename)
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        r = json.dumps(data, ensure_ascii=False, indent=2)
        await f.write(r)


async def get_sku_list(pageNo: int, pageSize: int):
    '''
    获取所有sku
    '''
    try:
        target = []
        for c1id, i in enumerate(path_list):
            async with aiofiles.open(i, 'r', encoding='utf-8') as f:
                data = await f.read()
                data = json.loads(data)
                r = parse_one_json(data, int(json_list[c1id].split('_')[0]))
                if r:
                    target.extend(r)
        total = len(target)
        start = (pageNo - 1) * pageSize
        end = start + pageSize  # 左闭右开
        result = target[start:end]
        if end > total:
            end = total
            result = target[start:]
        return {
            'data': result,
            'total': total,
            'pageNo': pageNo,
            'pageSize': pageSize,
            'start': start + 1,
            'end': end
        }
    except:
        return False


async def change_one_sku(c1id: int, c2id: int, c3id: int, c3num: int, skuNum: int, isShow: bool):
    '''
    修改某一sku
    都从1开始
    '''
    try:
        data = await get_c1_sku(c1id)
        c3name = list(data['contents'][c2id - 1][c3id].keys())[0]
        # 修改
        data['contents'][c2id-1][c3id][c3name][c3num -
                                               1]['skuInfo'][skuNum-1]['isShow'] = isShow
        # 重写原文件
        await set_c1_sku(c1id, data)
        return True
    except:
        return False


async def edit_one_sku(item: Item):
    '''
    编辑某个sku
    '''
    data = await get_c1_sku(item.c1id)
    c3name = list(data['contents'][item.c2id - 1][item.c3id].keys())[0]
    # 获取原来的sku信息
    t1 = data['contents'][item.c2id-1][item.c3id][c3name][item.num -
                                                          1]['skuInfo'][item.skuNum-1]
    # 整理要改的sku
    dic = item.dict()
    del dic['c1id']
    del dic['c2id']
    del dic['c3id']
    del dic['skuNum']
    del dic['num']
    dic['isShow'] = t1['isShow']  # 原来的状态
    # 替换
    data['contents'][item.c2id-1][item.c3id][c3name][item.num -
                                                          1]['skuInfo'][item.skuNum-1] = dic
    await set_c1_sku(item.c1id, data)
    return True


async def delete_one_sku(c1id: int, c2id: int, c3id: int, c3num: int, skuNum: int):
    '''
    删除某一sku
    '''
    data = await get_c1_sku(c1id)
    c3name = list(data['contents'][c2id - 1][c3id].keys())[0]
    # 删除
    data['contents'][c2id-1][c3id][c3name][c3num -
                                           1]['skuInfo'].pop(skuNum-1)
    # 重写原文件
    await set_c1_sku(c1id, data)
    return True
