"""
在庫エクスポートモジュール

ZAICOの在庫データをCSV形式でエクスポートする機能を提供します。
"""
import csv
import os
import sys
import logging
from datetime import datetime
from typing import Optional

from .api import get_zaico_inventories
from .config import INVENTORY_CSV_COLUMNS, setup_logging


# ロガーの設定
logger = setup_logging()


def get_app_dir() -> str:
    """
    アプリケーションのディレクトリパスを取得する

    exe化環境とスクリプト実行環境の両方に対応。

    Returns:
        str: アプリケーションのディレクトリパス
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def export_inventories_to_csv(filename: Optional[str] = None) -> bool:
    """
    在庫データをCSVファイルにエクスポートする

    Args:
        filename: 出力ファイル名（省略時は自動生成）

    Returns:
        bool: 処理の成功/失敗
    """
    inventories = get_zaico_inventories()
    if inventories is None:
        logger.error('在庫データ取得に失敗しました')
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
            writer.writerow(INVENTORY_CSV_COLUMNS)

            for item in inventories:
                writer.writerow([
                    item.get('id', ''),
                    item.get('title', ''),
                    item.get('category', ''),
                    item.get('place', ''),
                    item.get('state', ''),
                    item.get('quantity', ''),
                    item.get('unit', ''),
                    item.get('code', ''),
                    item.get('etc', ''),
                    item.get('updated_at', ''),
                    item.get('created_at', ''),
                    item.get('stocktake_attributes', {}).get('checked_at', ''),
                    item.get('group_tag', ''),
                    '',  # 仕入単価
                    ''   # 納品単価
                ])

        print(f'{filename} を出力しました')
        return True

    except Exception as e:
        logger.error(f'CSV書き込みエラー: {e}')
        return False


def main() -> None:
    """
    CSVエクスポートのエントリーポイント
    """
    export_inventories_to_csv()

