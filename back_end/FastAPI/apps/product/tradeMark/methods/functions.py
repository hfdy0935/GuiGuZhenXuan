# 商品品牌相关的操作
import json

def get_trade_mark_list() -> list:
    '''
    获取商品品牌信息列表
    '''
    with open('./data/product/tradeMark/tradeMarkList.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_trade_mark_list(trade_mark_list: list) -> None:
    '''
    保存商品品牌信息列表
    '''
    with open('./data/product/tradeMark/tradeMarkList.json', 'w', encoding='utf-8') as f:
        json.dump(trade_mark_list, f, ensure_ascii=False, indent=4)