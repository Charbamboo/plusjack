# PlusJack - ZAICO 在庫管理ツール

## 概要

ZAICO APIを利用した在庫管理ツール群です。以下の機能を提供します：

- **入庫処理**: 商品の入庫（数量加算）
- **出庫処理**: 商品の出庫（数量減算）
- **在庫エクスポート**: 在庫データのCSV出力
- **新規商品登録**: CSVファイルからの一括商品登録

## インストール方法

### 依存パッケージのインストール

```bash
cd src
pip install -r requirements.txt
```

### 環境変数の設定

プロジェクトルートまたは `src/` ディレクトリに `.env` ファイルを作成し、ZAICO APIトークンを設定してください：

```
ZAICO_API_TOKEN=your_api_token_here
```

## 使用方法

### 入庫処理

```bash
cd src
python zaico_stock_in.py 商品名 追加数量
```

例：
```bash
python zaico_stock_in.py "ボールペン黒" 100
```

### 出庫処理

```bash
cd src
python zaico_stock_out.py 商品名 出庫数量
```

例：
```bash
python zaico_stock_out.py "ボールペン黒" 50
```

### 在庫エクスポート

```bash
cd src
python export_zaico_inventory_csv.py
```

出力先: `src/tmp/inventory_export_YYYYMMDD_HHMMSS.csv`

### 新規商品登録

```bash
cd src
python register_new_items_to_zaico.py
```

入力CSVファイル: `src/tmp/new.csv`

CSVの形式：
```csv
物品名,カテゴリ,保管場所,状態,数量
商品A,カテゴリ1,倉庫A,新品,100
商品B,カテゴリ2,倉庫B,中古,50
```

## ファイル構成

```
plusjack/
├── src/
│   ├── zaico_stock_in.py              # 入庫処理エントリーポイント
│   ├── zaico_stock_out.py             # 出庫処理エントリーポイント
│   ├── export_zaico_inventory_csv.py  # エクスポートエントリーポイント
│   ├── register_new_items_to_zaico.py # 商品登録エントリーポイント
│   ├── requirements.txt               # 依存パッケージ
│   ├── zaico/                          # ZAICOパッケージ
│   │   ├── __init__.py                 # パッケージ初期化
│   │   ├── config.py                   # 設定・定数
│   │   ├── api.py                      # API通信処理
│   │   ├── stock_in.py                 # 入庫ロジック
│   │   ├── stock_out.py                # 出庫ロジック
│   │   ├── export_inventory.py         # エクスポートロジック
│   │   ├── register_items.py           # 登録ロジック
│   │   └── tests/                      # テストコード
│   │       ├── test_api.py
│   │       └── test_stock.py
│   ├── data/                           # マスターデータ
│   └── tmp/                            # 一時ファイル（入出力用）
├── README.md
└── .gitignore
```

### 各モジュールの役割

| モジュール | 責任 |
|-----------|------|
| `config.py` | API URL、トークン、ログ設定などの定数管理 |
| `api.py` | ZAICO APIとの通信処理 |
| `stock_in.py` | 入庫ロジック |
| `stock_out.py` | 出庫ロジック |
| `export_inventory.py` | CSVエクスポート処理 |
| `register_items.py` | 新規商品登録処理 |

## カスタマイズ方法

### API設定の変更

`src/zaico/config.py` を編集してください：

```python
# API設定
ZAICO_API_TOKEN = os.environ.get('ZAICO_API_TOKEN', '')
ZAICO_API_BASE_URL = 'https://web.zaico.co.jp/api/v1'

# ログ設定
LOG_FILE = 'error.log'
LOG_LEVEL = logging.ERROR
```

### CSVエクスポートのカラム変更

`src/zaico/config.py` の `INVENTORY_CSV_COLUMNS` を編集してください。

## テストの実行

```bash
cd src
python -m pytest zaico/tests/ -v
```

## EXE化（配布用）

```bash
cd src
pip install pyinstaller
pyinstaller zaico_stock_in.py --onefile --name zaico_stock_in
```

生成物: `src/dist/zaico_stock_in.exe`
