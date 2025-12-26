"""
ZAICO API 通信モジュール

ZAICOの在庫管理APIとの通信処理を担当するモジュールです。
在庫データの取得、更新、新規登録などの機能を提供します。
"""
import requests
import logging
from typing import Optional, List, Dict, Any, Tuple

from .config import ZAICO_API_TOKEN, ZAICO_API_BASE_URL, setup_logging


# ロガーの設定
logger = setup_logging()


def _get_headers() -> Dict[str, str]:
    """
    API通信用のヘッダーを取得する

    Returns:
        Dict[str, str]: Authorization と Content-Type を含むヘッダー
    """
    return {
        'Authorization': f'Bearer {ZAICO_API_TOKEN}',
        'Content-Type': 'application/json'
    }


def get_zaico_inventories() -> Optional[List[Dict[str, Any]]]:
    """
    ZAICOの現在の在庫一覧を取得する

    Returns:
        Optional[List[Dict[str, Any]]]: 在庫データのリスト。エラー時はNone
    """
    url = f'{ZAICO_API_BASE_URL}/inventories'
    response = requests.get(url, headers=_get_headers())

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f'Error: {response.status_code} - {response.text}')
        return None


def get_inventory_by_title(title: str) -> Optional[List[Dict[str, Any]]]:
    """
    タイトルで在庫データを絞り込み取得する

    Args:
        title: 検索する商品名

    Returns:
        Optional[List[Dict[str, Any]]]: マッチした在庫データのリスト。エラー時はNone
    """
    url = f'{ZAICO_API_BASE_URL}/inventories'
    params = {"title": title}
    response = requests.get(url, headers=_get_headers(), params=params)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f'Error: {response.status_code} - {response.text}')
        return None


def update_inventory_quantity(inventory_id: int, new_quantity: int) -> Optional[Dict[str, Any]]:
    """
    指定IDの在庫データの数量を更新する

    Args:
        inventory_id: 更新対象の在庫ID
        new_quantity: 新しい数量

    Returns:
        Optional[Dict[str, Any]]: 更新後の在庫データ。エラー時はNone
    """
    url = f'{ZAICO_API_BASE_URL}/inventories/{inventory_id}'
    data = {"quantity": str(new_quantity)}
    response = requests.put(url, headers=_get_headers(), json=data)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f'Error: {response.status_code} - {response.text}')
        return None


def create_inventory(
    title: str,
    category: Optional[str] = None,
    place: Optional[str] = None,
    state: Optional[str] = None,
    quantity: Optional[int] = None
) -> Tuple[bool, Any]:
    """
    ZAICO APIに新規在庫を登録する

    Args:
        title: 物品名（必須）
        category: カテゴリ
        place: 保管場所
        state: 状態
        quantity: 数量

    Returns:
        Tuple[bool, Any]: (成功フラグ, レスポンスデータまたはエラーメッセージ)
    """
    url = f'{ZAICO_API_BASE_URL}/inventories'
    payload: Dict[str, Any] = {"title": title}

    if category:
        payload["category"] = category
    if place:
        payload["place"] = place
    if state:
        payload["state"] = state
    if quantity is not None:
        payload["quantity"] = str(quantity)

    response = requests.post(url, headers=_get_headers(), json=payload)

    if response.status_code == 200:
        return True, response.json()
    else:
        logger.error(f'新規在庫登録失敗: {response.status_code}, {response.text}')
        return False, response.text

