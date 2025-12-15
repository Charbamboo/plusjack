import csv
from zaico_api import get_zaico_inventories
from datetime import datetime
import logging
import os
import sys
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# 出力するCSVのカラム名（@inventory_export_xxx.csvに合わせる）
COLUMNS = [
    '在庫ID','物品名','カテゴリ','保管場所','状態','数量','単位','QRコード・バーコードの値',
    '備考','更新日','作成日','棚卸日','グループタグ','仕入単価','納品単価'
]

def get_app_dir():
    if getattr(sys, 'frozen', False):  # exe化環境
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def export_inventories_to_csv(filename=None):
    inventories = get_zaico_inventories()
    if inventories is None:
        logging.error('在庫データ取得に失敗しました')
        return False
    # exe/py両対応の出力先ディレクトリ（../tmp）
    output_dir = os.path.abspath(os.path.join(get_app_dir(), '../tmp'))
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        dstr = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f'inventory_export_{dstr}.csv')
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)
            for item in inventories:
                writer.writerow([
                    item.get('id',''),
                    item.get('title',''),
                    item.get('category',''),
                    item.get('place',''),
                    item.get('state',''),
                    item.get('quantity',''),
                    item.get('unit',''),
                    item.get('code',''),
                    item.get('etc',''),
                    item.get('updated_at',''),
                    item.get('created_at',''),
                    item.get('stocktake_attributes',{}).get('checked_at',''),
                    item.get('group_tag',''),
                    '',  # 仕入単価
                    ''   # 納品単価
                ])
        print(f'{filename} を出力しました')
        return True
    except Exception as e:
        logging.error(f'CSV書き込みエラー: {e}')
        return False

if __name__ == '__main__':
    export_inventories_to_csv()
