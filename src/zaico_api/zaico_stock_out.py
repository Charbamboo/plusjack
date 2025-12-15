import sys
from zaico_api import get_inventory_by_title, update_inventory_quantity
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def stock_out(title, sub_quantity):
    """
    指定タイトルの商品を出庫（sub_quantity分減算）
    在庫不足時もログは出すが在庫は減算・更新する
    """
    items = get_inventory_by_title(title)
    if not items:
        logging.error(f'商品「{title}」が見つかりません')
        return False
    inventory = items[0]
    inventory_id = inventory['id']
    try:
        now_quantity = float(inventory['quantity'])
    except Exception as e:
        logging.error(f'在庫数の変換に失敗: {inventory["quantity"]} ({e})')
        return False
    try:
        sub_quantity_f = float(sub_quantity)
    except Exception as e:
        logging.error(f'出庫入力値の変換に失敗: {sub_quantity} ({e})')
        return False
    if now_quantity < sub_quantity_f:
        logging.error(f'在庫不足: 現在の数量({now_quantity}) < 出庫依頼({sub_quantity_f})')
        # 在庫不足でも減算・更新は実施
    new_quantity = int(now_quantity - sub_quantity_f)
    result = update_inventory_quantity(inventory_id, new_quantity)
    if result:
        print(f'出庫完了（商品: {title}、新数量: {new_quantity}）')
        return True
    else:
        logging.error('出庫に失敗しました')
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('使い方: python zaico_stock_out.py 商品名 出庫数量(int)')
        sys.exit(1)
    title = sys.argv[1]
    sub_quantity = sys.argv[2]
    stock_out(title, sub_quantity)
