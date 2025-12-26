"""
入庫処理モジュール

ZAICOの在庫に対する入庫（数量加算）処理を行います。
"""
import sys
import logging

from .api import get_inventory_by_title, update_inventory_quantity
from .config import setup_logging


# ロガーの設定
logger = setup_logging()


def stock_in(title: str, add_quantity: str) -> bool:
    """
    指定タイトルの商品に入庫（add_quantity分加算）する

    Args:
        title: 商品名
        add_quantity: 追加する数量（文字列）

    Returns:
        bool: 処理の成功/失敗
    """
    items = get_inventory_by_title(title)
    if not items:
        logger.error(f'商品「{title}」が見つかりません')
        return False

    inventory = items[0]
    inventory_id = inventory['id']

    # 現在の数量を取得
    try:
        now_quantity = float(inventory['quantity'])
    except (ValueError, TypeError) as e:
        logger.error(f'在庫数の変換に失敗: {inventory["quantity"]} ({e})')
        return False

    # 追加数量を変換
    try:
        add_quantity_f = float(add_quantity)
    except (ValueError, TypeError) as e:
        logger.error(f'追加入力値の変換に失敗: {add_quantity} ({e})')
        return False

    new_quantity = int(now_quantity + add_quantity_f)
    result = update_inventory_quantity(inventory_id, new_quantity)

    if result:
        print(f'入庫完了（商品: {title}、新数量: {new_quantity}）')
        return True
    else:
        logger.error('入庫に失敗しました')
        return False


def main() -> None:
    """
    入庫処理のエントリーポイント

    コマンドライン引数から商品名と追加数量を受け取り、入庫処理を実行する。
    """
    if len(sys.argv) != 3:
        print('使い方: python zaico_stock_in.py 商品名 追加数量(int)')
        sys.exit(1)

    title = sys.argv[1]
    add_quantity = sys.argv[2]
    stock_in(title, add_quantity)
