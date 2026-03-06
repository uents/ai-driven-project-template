"""E2Eテスト: API エンドツーエンドテスト"""

import os
import uuid

import pytest
import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "https://staging-api.example.com")


class TestUserApiE2E:
    """ユーザーAPIのE2Eテスト"""

    def test_ユーザー作成と取得の一連フロー(self):
        """ユーザーを作成し、そのユーザーを取得できることを検証する"""
        # Given: 有効なユーザーデータ
        user_data = {
            "name": "E2Eテストユーザー",
            "email": f"e2e-test-{uuid.uuid4()}@example.com",
        }

        # When: ユーザーを作成
        create_response = requests.post(f"{API_BASE_URL}/users", json=user_data)

        # Then: 201が返却される
        assert create_response.status_code == 201
        created_user = create_response.json()
        assert created_user["name"] == user_data["name"]

        # When: 作成したユーザーを取得
        get_response = requests.get(f"{API_BASE_URL}/users/{created_user['user_id']}")

        # Then: 200でユーザー情報が返却される
        assert get_response.status_code == 200
        fetched_user = get_response.json()
        assert fetched_user["user_id"] == created_user["user_id"]

    def test_存在しないユーザーの取得(self):
        """存在しないユーザーIDで404が返却されることを検証する"""
        # Given: 存在しないユーザーID
        fake_user_id = str(uuid.uuid4())

        # When: 存在しないユーザーを取得
        response = requests.get(f"{API_BASE_URL}/users/{fake_user_id}")

        # Then: 404が返却される
        assert response.status_code == 404
