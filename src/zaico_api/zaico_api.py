from dotenv import load_dotenv
import os
import requests
import logging


# APIアクセスキーの設定
load_dotenv()
ZAICO_API_TOKEN = os.environ['ZAICO_API_TOKEN']

# ログ設定
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def get_zaico_inventories():
    """
    ZAICOの現在の在庫一覧を取得する
    returns: list of inventory dict
    """
    BASE_URL = 'https://web.zaico.co.jp/api/v1/inventories'
    headers = {
        'Authorization': f'Bearer {ZAICO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f'Error: {response.status_code} - {response.text}')
        return None


def get_inventory_by_title(title):
    """タイトルで在庫データを絞り込み取得"""
    BASE_URL = 'https://web.zaico.co.jp/api/v1/inventories'
    headers = {
        'Authorization': f'Bearer {ZAICO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    params = {"title": title}
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json()
        return items
    else:
        logging.error(f'Error: {response.status_code} - {response.text}')
        return None

def update_inventory_quantity(inventory_id, new_quantity):
    """指定IDの在庫データの数量を更新"""
    BASE_URL = f'https://web.zaico.co.jp/api/v1/inventories/{inventory_id}'
    headers = {
        'Authorization': f'Bearer {ZAICO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {"quantity": str(new_quantity)}
    response = requests.put(BASE_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f'Error: {response.status_code} - {response.text}')
        return None


def create_inventory(title, category=None, place=None, state=None, quantity=None):
    """
    ZAICO APIの在庫（inventory）新規登録: POST /api/v1/inventories
    必須: title
    任意: category, place, state, quantity
    """
    BASE_URL = 'https://web.zaico.co.jp/api/v1/inventories'
    headers = {
        'Authorization': f'Bearer {ZAICO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {"title": title}
    if category: payload["category"] = category
    if place: payload["place"] = place
    if state: payload["state"] = state
    if quantity is not None: payload["quantity"] = str(quantity)
    response = requests.post(BASE_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        logging.error(f'新規在庫登録失敗: {response.status_code}, {response.text}')
        return False, response.text


if __name__ == '__main__':
    inventories = get_zaico_inventories()
    if inventories is not None:
        print('在庫一覧:')
        for item in inventories:
            print(item)
    else:
        print('在庫一覧の取得に失敗しました')

