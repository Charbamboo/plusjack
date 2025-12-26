"""
ZAICO API モジュールのテスト

API関連機能のユニットテストを提供します。
モックを使用して実際のAPI呼び出しを行わずにテストします。
"""
import pytest
from unittest.mock import patch, Mock

from zaico.api import (
    get_zaico_inventories,
    get_inventory_by_title,
    update_inventory_quantity,
    create_inventory
)


class TestGetZaicoInventories:
    """get_zaico_inventories関数のテスト"""

    @patch('zaico.api.requests.get')
    def test_success(self, mock_get):
        """正常に在庫一覧を取得できる"""
        expected_data = [
            {'id': 1, 'title': '商品A', 'quantity': '10'},
            {'id': 2, 'title': '商品B', 'quantity': '20'}
        ]
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: expected_data
        )

        result = get_zaico_inventories()

        assert result == expected_data
        mock_get.assert_called_once()

    @patch('zaico.api.requests.get')
    def test_error(self, mock_get):
        """APIエラー時にNoneを返す"""
        mock_get.return_value = Mock(
            status_code=500,
            text='Internal Server Error'
        )

        result = get_zaico_inventories()

        assert result is None


class TestGetInventoryByTitle:
    """get_inventory_by_title関数のテスト"""

    @patch('zaico.api.requests.get')
    def test_success(self, mock_get):
        """タイトルで在庫を検索できる"""
        expected_data = [{'id': 1, 'title': '商品A', 'quantity': '10'}]
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: expected_data
        )

        result = get_inventory_by_title('商品A')

        assert result == expected_data
        mock_get.assert_called_once()

    @patch('zaico.api.requests.get')
    def test_not_found(self, mock_get):
        """該当する在庫がない場合は空リストを返す"""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: []
        )

        result = get_inventory_by_title('存在しない商品')

        assert result == []


class TestUpdateInventoryQuantity:
    """update_inventory_quantity関数のテスト"""

    @patch('zaico.api.requests.put')
    def test_success(self, mock_put):
        """在庫数量を正常に更新できる"""
        expected_data = {'id': 1, 'title': '商品A', 'quantity': '15'}
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: expected_data
        )

        result = update_inventory_quantity(1, 15)

        assert result == expected_data
        mock_put.assert_called_once()

    @patch('zaico.api.requests.put')
    def test_error(self, mock_put):
        """更新失敗時にNoneを返す"""
        mock_put.return_value = Mock(
            status_code=404,
            text='Not Found'
        )

        result = update_inventory_quantity(999, 10)

        assert result is None


class TestCreateInventory:
    """create_inventory関数のテスト"""

    @patch('zaico.api.requests.post')
    def test_success(self, mock_post):
        """新規在庫を正常に登録できる"""
        expected_data = {'id': 3, 'title': '新商品', 'quantity': '5'}
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: expected_data
        )

        success, result = create_inventory('新商品', quantity=5)

        assert success is True
        assert result == expected_data
        mock_post.assert_called_once()

    @patch('zaico.api.requests.post')
    def test_with_optional_params(self, mock_post):
        """オプションパラメータ付きで登録できる"""
        expected_data = {
            'id': 4,
            'title': '商品C',
            'category': 'カテゴリA',
            'place': '倉庫1',
            'state': '新品',
            'quantity': '100'
        }
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: expected_data
        )

        success, result = create_inventory(
            '商品C',
            category='カテゴリA',
            place='倉庫1',
            state='新品',
            quantity=100
        )

        assert success is True
        assert result == expected_data

    @patch('zaico.api.requests.post')
    def test_error(self, mock_post):
        """登録失敗時にFalseとエラーメッセージを返す"""
        mock_post.return_value = Mock(
            status_code=400,
            text='Bad Request'
        )

        success, result = create_inventory('不正なデータ')

        assert success is False
        assert 'Bad Request' in result

