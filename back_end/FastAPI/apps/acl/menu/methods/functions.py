import json
import aiofiles
from .types import AddMenuModel


async def get_all_menu_main() -> list:
    '''
    获取所有菜单
    '''
    async with aiofiles.open('./data/acl/menu/allMenu.json', 'r', encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)


async def set_all_menu_main(value: list) -> None:
    '''
    写入所有菜单
    '''
    async with aiofiles.open('./data/acl/menu/allMenu.json', 'w', encoding='utf-8') as f:
        data = json.dumps(value, ensure_ascii=False, indent=2)
        await f.write(data)


async def get_one_item(id_: str):
    '''
    根据id获取对应的菜单字典
    '''
    data = await get_all_menu_main()

    def f(data: list):
        for i in data:
            if i['id'] == id_:
                return i
            if i['children']:
                result = f(i['children'])
                if result:
                    return result
        return None
    return f(data)


async def add_menu(item: AddMenuModel):
    '''
    添加菜单
    '''
    data = await get_all_menu_main()
    dic = item.dict()
    now_item = await get_one_item(item.id_)
    if not now_item:
        return False
    # 如果菜单名重复
    if item.name in [i['name'] for i in now_item['children']]:
        return '菜单名不能重复'

    # id前缀
    # 考虑添加第一个子菜单的情况
    prefix = now_item['id']
    # id最后一个
    postfix = eval(now_item['children'][-1]['id'].split('.')
                   [-1]) if now_item['children'] else 0
    new_id = prefix + '.' + str(postfix + 1)
    del dic['id_']
    dic = {
        **dic,
        'id': new_id,
        'pid': 0,
        'toCode': None,
        'type': 1,
        'status': None,
        'children': []
    }
    now_item_copy = str(now_item)  # 复制，字符串
    now_item['children'].append(dic)  # 添加
    t1 = str(data)  # 总的，字符串
    t1 = t1.replace(now_item_copy, str(now_item))  # 字符串替换
    await set_all_menu_main(eval(t1))  # 重新写入
    return True


async def edit_menu(item: AddMenuModel):
    '''
    修改菜单
    '''
    data = await get_all_menu_main()
    now_item = await get_one_item(item.id_)
    if not now_item:
        return False
    # 如果修改的是一级，不存在菜单名重复的情况
    if item.level == 1:
        now_item['name'] = item.name
        now_item['code'] = item.code
        await set_all_menu_main([now_item])
        return '修改成功'

    # 如果修改的是二级或三级菜单，且它的父菜单只有它一个子菜单，也不存在菜单名重复的情况
    p = item.id_.split('.')[:-1]  # 要修改的菜单的父级菜单
    father_id = str(p[0]) if len(p) == 1 else '.'.join(p)
    father_item = await get_one_item(father_id)
    if father_item:
        if len(father_item['children']) == 1:
            now_item_copy = str(now_item)  # 复制，字符串
            now_item['name'] = item.name
            now_item['code'] = item.code
            t1 = str(data)  # 总的，字符串
            t1 = t1.replace(now_item_copy, str(now_item), )  # 字符串替换
            await set_all_menu_main(eval(t1))  # 重新写入
            return '修改成功'

        # 其他情况需要判断是否菜单名是否重复，排除自己原来的name
        brothers_name = [i['name']
                         for i in father_item['children'] if i['id'] != item.id_]
        if item.name in brothers_name:
            return '菜单名不能重复'

        # 没有重复的
        now_item_copy = str(now_item)  # 复制，字符串
        now_item['name'] = item.name
        now_item['code'] = item.code
        t1 = str(data)  # 总的，字符串
        t1 = t1.replace(now_item_copy, str(now_item))  # 字符串替换
        await set_all_menu_main(eval(t1))  # 重新写入
        return '修改成功'
    return False


async def delete_menu(id_: str):
    '''
    删除菜单
    '''
    data = await get_all_menu_main()
    t1 = str(data)
    now_item = await get_one_item(id_)

    # 如果是一级菜单，直接删
    if id_ == '1':
        await set_all_menu_main([])
        return True
    
    # 判断父菜单有几个子菜单
    p = id_.split('.')[:-1]
    father_id = str(p[0]) if len(p) == 1 else '.'.join(p)
    father_item = await get_one_item(father_id)

    if father_item:
        # 如果只有一个，或有多个但是最后一个，可以直接删
        if len(father_item['children']) == 1 or (father_item['children'][-1]['id'] == id_):
            t1 = t1.replace(str(now_item), '')
        # 如果原来有多个还不在最后，需要把后面的","一起删了
        else:
            t1 = t1.replace(str(now_item) + ',', '')
    await set_all_menu_main(eval(t1))
    return True
