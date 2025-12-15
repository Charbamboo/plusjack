import csv
from zaico_api import create_inventory
import os
import sys

def get_app_dir():
    if getattr(sys, 'frozen', False):  # exe化環境
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def main():
    app_dir = get_app_dir()
    csv_path = os.path.abspath(os.path.join(app_dir, '../tmp/new.csv'))
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("物品名", "")
            if not title:
                continue
            category = row.get("カテゴリ")
            place = row.get("保管場所")
            state = row.get("状態")
            quantity = row.get("数量")
            # 空欄→None
            for k in ["category", "place", "state", "quantity"]:
                if locals()[k] == "":
                    locals()[k] = None
            ok, resp = create_inventory(title, category, place, state, quantity)
            if ok:
                print(f'登録成功: {title}')
            else:
                print(f'登録失敗: {title} [{resp}]')

if __name__ == "__main__":
    main()
