"""
ZAICO API 設定・定数モジュール

このモジュールはZAICO APIとの通信に必要な設定値と
アプリケーション全体で使用する定数を管理します。
"""
import os
import logging
from dotenv import load_dotenv


# 環境変数の読み込み
load_dotenv()

# API設定
ZAICO_API_TOKEN = os.environ.get('ZAICO_API_TOKEN', '')
ZAICO_API_BASE_URL = 'https://web.zaico.co.jp/api/v1'

# ログ設定
LOG_FILE = 'error.log'
LOG_LEVEL = logging.ERROR
LOG_FORMAT = '%(asctime)s %(levelname)s:%(message)s'

# CSVエクスポート用カラム定義
INVENTORY_CSV_COLUMNS = [
    '在庫ID', '物品名', 'カテゴリ', '保管場所', '状態', '数量', '単位',
    'QRコード・バーコードの値', '備考', '更新日', '作成日', '棚卸日',
    'グループタグ', '仕入単価', '納品単価'
]


def setup_logging() -> logging.Logger:
    """
    ロギングを設定し、ロガーを返す

    Returns:
        logging.Logger: 設定済みのロガー
    """
    logging.basicConfig(
        filename=LOG_FILE,
        level=LOG_LEVEL,
        format=LOG_FORMAT
    )
    return logging.getLogger(__name__)

