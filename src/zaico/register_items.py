"""
新規商品登録モジュール

CSVファイルから新規商品をZAICOに一括登録する機能を提供します。
"""
import csv
import os
import sys
from typing import Optional

from .api import create_inventory


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


def _convert_empty_to_none(value: Optional[str]) -> Optional[str]:
    """
    空文字をNoneに変換する

    Args:
        value: 変換対象の値

    Returns:
        Optional[str]: 空文字の場合はNone、それ以外は元の値
    """
    return None if value == "" else value


def register_items_from_csv(csv_path: Optional[str] = None) -> None:
    """
    CSVファイルから商品を読み込み、ZAICOに登録する

    Args:
        csv_path: 入力CSVファイルのパス（省略時はデフォルトパス）
    """
    if csv_path is None:
        app_dir = get_app_dir()
        csv_path = os.path.abspath(os.path.join(app_dir, '../tmp/new.csv'))

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row.get("物品名", "")
            if not title:
                continue

            category = _convert_empty_to_none(row.get("カテゴリ"))
            place = _convert_empty_to_none(row.get("保管場所"))
            state = _convert_empty_to_none(row.get("状態"))
            quantity = _convert_empty_to_none(row.get("数量"))

            ok, resp = create_inventory(title, category, place, state, quantity)

            if ok:
                print(f'登録成功: {title}')
            else:
                print(f'登録失敗: {title} [{resp}]')


def main() -> None:
    """
    商品登録処理のエントリーポイント
    """
    register_items_from_csv()

