import sys
from zaico_api import get_inventory_by_title, update_inventory_quantity
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def stock_in(title, add_quantity):
    """
    指定タイトルの商品に入庫（add_quantity分加算）
    """
    items = get_inventory_by_title(title)
    if not items:
        logging.error(f'商品「{title}」が見つかりません')
        return False
    inventory = items[0]
    inventory_id = inventory['id']
    # ここをfloatで受けて、加算後はintに丸めて管理
    try:
        now_quantity = float(inventory['quantity'])
    except Exception as e:
        logging.error(f'在庫数の変換に失敗: {inventory["quantity"]} ({e})')
        return False
    try:
        add_quantity_f = float(add_quantity)
    except Exception as e:
        logging.error(f'追加入力値の変換に失敗: {add_quantity} ({e})')
        return False
    new_quantity = int(now_quantity + add_quantity_f)
    result = update_inventory_quantity(inventory_id, new_quantity)
    if result:
        print(f'入庫完了（商品: {title}、新数量: {new_quantity}）')
        return True
    else:
        logging.error('入庫に失敗しました')
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('使い方: python zaico_stock_in.py 商品名 追加数量(int)')
        sys.exit(1)
    title = sys.argv[1]
    add_quantity = sys.argv[2]
    stock_in(title, add_quantity)
