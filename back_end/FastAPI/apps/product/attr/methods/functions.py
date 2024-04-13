import json
import aiofiles


async def get_attr_category(level: int, c1id: int = 0, c2id: int = 0) -> list:
    '''
    根据分类等级和id获取数据
    从1开始
    '''
    async with aiofiles.open('./data/product/attr/attrCategory.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        attr_category_list = json.loads(data)
        # 只获取一级分类
        if level == 1:
            return [item['title'] for item in attr_category_list]
        elif level == 2:
            return [item[0] for item in attr_category_list[c1id-1]['contents']]
        elif level == 3:
            return [item for item in attr_category_list[c1id-1]['contents'][c2id-1][1:]]
        return []


async def get_attr_list_main():
    '''
    获取attrList.json中的属性
    原始，格式仅限本模块中用
    '''
    async with aiofiles.open('./data/product/attr/attrList.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)


async def set_attr_list_main(value: dict):
    '''
    修改attrList.json中的属性
    '''
    async with aiofiles.open('./data/product/attr/attrList.json', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def get_attr_list(c1id: int, c2id: int, c3id: int, pageNo: int, pageSize: int):
    '''
    根据三级分类的id返回对应属性
    从1开始
    '''
    attr_list = await get_attr_list_main()
    data = list(attr_list[c1id - 1]['contents'][c2id - 1][c3id].values())[0]
    start = (pageNo - 1) * pageSize
    end = start + pageSize  # 左闭右开
    if end >= len(data):
        end = len(data)
    return {
        'data': data[start:end],
        'total': len(data),
        'pageNo': pageNo,
        'pageSize': pageSize,
        'start': start + 1,
        'end': end
    }


async def delete_one_attr(c1id: int, c2id: int, c3id: int, index: int):
    '''
    根据索引删除某个属性
    从1开始
    '''
    try:
        attr_list = await get_attr_list_main()
        attr_name = list(attr_list[c1id - 1]['contents'][c2id - 1][c3id])[0]
        del attr_list[c1id - 1]['contents'][c2id -
                                            1][c3id][attr_name][index - 1]
        await set_attr_list_main(attr_list)
        return True
    except:
        return False


async def add_one_attr(c1id: int, c2id: int, c3id: int, name: str, value: list[str]):
    '''
    根据三级分类，找到对应位置
    末尾添加一个属性
    '''
    attr_list = await get_attr_list_main()
    attr_name = list(attr_list[c1id - 1]['contents'][c2id - 1][c3id])[0]
    attr_list[c1id - 1]['contents'][c2id -
                                    1][c3id][attr_name].append({name: value})
    await set_attr_list_main(attr_list)
    return True


async def edit_one_attr(c1id: int, c2id: int, c3id: int, index: int, name: str, value: list[str]):
    '''
    根据索引修改某个属性
    从1开始
    '''
    attr_list = await get_attr_list_main()
    attr_name = list(attr_list[c1id - 1]['contents'][c2id - 1][c3id])[0]
    attr_list[c1id - 1]['contents'][c2id -
                                    1][c3id][attr_name][index - 1] = {name: value}
    await set_attr_list_main(attr_list)
    return True
