"""
出庫処理モジュール

ZAICOの在庫に対する出庫（数量減算）処理を行います。
"""
import sys
import logging

from .api import get_inventory_by_title, update_inventory_quantity
from .config import setup_logging


# ロガーの設定
logger = setup_logging()


def stock_out(title: str, sub_quantity: str) -> bool:
    """
    指定タイトルの商品を出庫（sub_quantity分減算）する

    在庫不足時もログは出すが在庫は減算・更新する。

    Args:
        title: 商品名
        sub_quantity: 出庫する数量（文字列）

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

    # 出庫数量を変換
    try:
        sub_quantity_f = float(sub_quantity)
    except (ValueError, TypeError) as e:
        logger.error(f'出庫入力値の変換に失敗: {sub_quantity} ({e})')
        return False

    # 在庫不足チェック（警告のみ、処理は続行）
    if now_quantity < sub_quantity_f:
        logger.error(f'在庫不足: 現在の数量({now_quantity}) < 出庫依頼({sub_quantity_f})')

    new_quantity = int(now_quantity - sub_quantity_f)
    result = update_inventory_quantity(inventory_id, new_quantity)

    if result:
        print(f'出庫完了（商品: {title}、新数量: {new_quantity}）')
        return True
    else:
        logger.error('出庫に失敗しました')
        return False


def main() -> None:
    """
    出庫処理のエントリーポイント

    コマンドライン引数から商品名と出庫数量を受け取り、出庫処理を実行する。
    """
    if len(sys.argv) != 3:
        print('使い方: python zaico_stock_out.py 商品名 出庫数量(int)')
        sys.exit(1)

    title = sys.argv[1]
    sub_quantity = sys.argv[2]
    stock_out(title, sub_quantity)

