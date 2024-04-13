import json
import os
import aiofiles
from ..methods.types import Item


async def get_sku_info_before_add_main(c1id: int):
    '''
    获取对应一级分类json中的属性
    '''
    c1_list = os.listdir('./data/product/spu/skuInSpuBeforeAdd')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/skuInSpuBeforeAdd/{c1_name}', 'r', encoding='utf-8') as f:
        spu_list = json.loads(await f.read())
        return spu_list


async def set_sku_info_before_add_main(c1id, value: dict):
    '''
    修改对应一级分类json中的属性
    '''
    c1_list = os.listdir('./data/product/spu/skuInSpuBeforeAdd')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/skuInSpuBeforeAdd/{c1_name}', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def get_sku_list_before_add(c1id: int, c2id: int, c3id: int, num: int):
    '''
    给某个spu添加sku之前获取的数据
    '''
    try:
        sku_list = await get_sku_info_before_add_main(c1id)
        data = list(sku_list['contents'][c2id - 1][c3id].values())[0][num-1]
        return data
    except:
        return False


namelist = ['10_食品_酒类_生鲜_特产.json',
            '11_艺术_礼品鲜花_农资绿箱.json',
            '12_医药保健_计生情趣.json',
            '13_图书_文娱_教育_电子书.json',
            '14_机票_酒店_旅游_生活.json',
            '15_众筹_白条_保险_企业金融.json',
            '16_安装_维修_清洗_二手.json',
            '1_手机_运营商_数码.json',
            '2_电脑_办公.json',
            '3_家具_家居_家装_厨具.json',
            '4_男装_女装_童装_内衣.json',
            '5_美妆_个护清洁_宠物.json',
            '6_女鞋_箱包_钟表_珠宝.json',
            '7_男鞋_运动_户外.json',
            '8_房产_汽车_汽车用品.json',
            '9_母婴_玩具_乐器.json']


async def get_add_sku_info_main(c1id: int):
    '''
    获取对应一级分类json中添加了的sku
    '''
    c1_list = os.listdir('./data/product/spu/addSkuList')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/addSkuList/{c1_name}', 'r', encoding='utf-8') as f:
        sku_list = json.loads(await f.read())
        return sku_list


async def set_add_sku_info_main(c1id: int, value: dict):
    '''
    修改对应一级分类json中添加了的sku
    '''
    c1_list = os.listdir('./data/product/spu/addSkuList')
    c1_name = [i for i in c1_list if i.split('_')[0] == str(c1id)][0]
    async with aiofiles.open(f'./data/product/spu/addSkuList/{c1_name}', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def add_sku(item: Item):
    '''
    正式添加sku
    '''
    try:
        c1id = item.c1id
        c2id = item.c2id
        c3id = item.c3id
        num = item.num
        add_sku_list = await get_add_sku_info_main(c1id)
        c3_name = list(add_sku_list['contents'][c2id - 1][c3id].keys())[0]
        del item.c1id
        del item.c2id
        del item.c3id
        del item.num
        t = item.dict()
        t['isShow'] = False

        add_sku_list['contents'][c2id-1][c3id][c3_name][num -
                                                        1]['skuInfo'].append(t)
        print(add_sku_list['contents'][c2id-1][c3id][c3_name][num-1])
        await set_add_sku_info_main(c1id, add_sku_list)
        return True
    except:
        return False


async def view_sku(c1id: int, c2id: int, c3id: int, num: int):
    '''
    查看spu对应的sku详情
    '''
    try:
        add_sku_list = await get_add_sku_info_main(c1id)
        c3_name = list(add_sku_list['contents'][c2id - 1][c3id].keys())[0]
        data = add_sku_list['contents'][c2id - 1][c3id][c3_name][num-1]['skuInfo']
        for index,_ in enumerate(data):
            data[index]['序号'] = index+1
        return data
    except:
        return False
