"""
入庫処理エントリーポイント

ZAICOの在庫に対する入庫処理を実行します。

使用方法:
    python zaico_stock_in.py 商品名 追加数量
"""
from zaico.stock_in import main

if __name__ == "__main__":
    main()

