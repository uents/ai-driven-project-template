"""ハンドラーのユニットテスト"""

import json

import pytest


class TestCreateUserHandler:
    """ユーザー作成ハンドラーのテスト"""

    def test_ユーザー作成_正常系(self):
        """有効なリクエストでユーザーが作成されること"""
        # Given: 有効なユーザーデータ
        event = {
            "httpMethod": "POST",
            "path": "/users",
            "body": json.dumps({"name": "田中太郎", "email": "tanaka@example.com"}),
        }

        # When: ハンドラーを実行
        # TODO: ハンドラーの実行とモックのセットアップ

        # Then: 201が返却される
        pass

    def test_ユーザー作成_名前が空の場合_400エラー(self):
        """名前が空の場合にバリデーションエラーとなること"""
        # Given: 名前が空のリクエスト
        event = {
            "httpMethod": "POST",
            "path": "/users",
            "body": json.dumps({"name": "", "email": "tanaka@example.com"}),
        }

        # When: ハンドラーを実行
        # TODO: ハンドラーの実行

        # Then: 400が返却される
        pass

    def test_ユーザー作成_メール重複の場合_409エラー(self):
        """メールアドレスが重複している場合に409エラーとなること"""
        # Given: 既に登録済みのメールアドレス

        # When: 同じメールアドレスでユーザー作成を実行

        # Then: 409が返却される
        pass
