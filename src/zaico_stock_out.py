"""
出庫処理エントリーポイント

ZAICOの在庫に対する出庫処理を実行します。

使用方法:
    python zaico_stock_out.py 商品名 出庫数量
"""
from zaico.stock_out import main

if __name__ == "__main__":
    main()

