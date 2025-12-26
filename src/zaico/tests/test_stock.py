"""
入出庫処理モジュールのテスト

stock_in, stock_out 関数のユニットテストを提供します。
"""
import pytest
from unittest.mock import patch, Mock

from zaico.stock_in import stock_in
from zaico.stock_out import stock_out


class TestStockIn:
    """stock_in関数のテスト"""

    @patch('zaico.stock_in.update_inventory_quantity')
    @patch('zaico.stock_in.get_inventory_by_title')
    def test_success(self, mock_get, mock_update):
        """正常に入庫できる"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': '10'}]
        mock_update.return_value = {'id': 1, 'quantity': '15'}

        result = stock_in('商品A', '5')

        assert result is True
        mock_update.assert_called_once_with(1, 15)

    @patch('zaico.stock_in.get_inventory_by_title')
    def test_item_not_found(self, mock_get):
        """商品が見つからない場合はFalseを返す"""
        mock_get.return_value = []

        result = stock_in('存在しない商品', '5')

        assert result is False

    @patch('zaico.stock_in.get_inventory_by_title')
    def test_invalid_quantity_format(self, mock_get):
        """在庫数が不正な形式の場合はFalseを返す"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': 'invalid'}]

        result = stock_in('商品A', '5')

        assert result is False

    @patch('zaico.stock_in.get_inventory_by_title')
    def test_invalid_add_quantity(self, mock_get):
        """追加数量が不正な形式の場合はFalseを返す"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': '10'}]

        result = stock_in('商品A', 'invalid')

        assert result is False


class TestStockOut:
    """stock_out関数のテスト"""

    @patch('zaico.stock_out.update_inventory_quantity')
    @patch('zaico.stock_out.get_inventory_by_title')
    def test_success(self, mock_get, mock_update):
        """正常に出庫できる"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': '10'}]
        mock_update.return_value = {'id': 1, 'quantity': '7'}

        result = stock_out('商品A', '3')

        assert result is True
        mock_update.assert_called_once_with(1, 7)

    @patch('zaico.stock_out.update_inventory_quantity')
    @patch('zaico.stock_out.get_inventory_by_title')
    def test_insufficient_stock(self, mock_get, mock_update):
        """在庫不足でも出庫は実行される"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': '5'}]
        mock_update.return_value = {'id': 1, 'quantity': '-5'}

        result = stock_out('商品A', '10')

        # 在庫不足でも処理は成功する
        assert result is True
        mock_update.assert_called_once_with(1, -5)

    @patch('zaico.stock_out.get_inventory_by_title')
    def test_item_not_found(self, mock_get):
        """商品が見つからない場合はFalseを返す"""
        mock_get.return_value = []

        result = stock_out('存在しない商品', '5')

        assert result is False

    @patch('zaico.stock_out.update_inventory_quantity')
    @patch('zaico.stock_out.get_inventory_by_title')
    def test_update_failed(self, mock_get, mock_update):
        """更新に失敗した場合はFalseを返す"""
        mock_get.return_value = [{'id': 1, 'title': '商品A', 'quantity': '10'}]
        mock_update.return_value = None

        result = stock_out('商品A', '3')

        assert result is False

