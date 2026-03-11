"""リポジトリのユニットテスト"""

import boto3
import pytest
from moto import mock_dynamodb

from model import User
from repository import UserRepository


@pytest.fixture
def dynamodb_table():
    """テスト用DynamoDBテーブルのセットアップ"""
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        table = dynamodb.create_table(
            TableName="test-table",
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GSI1PK", "AttributeType": "S"},
                {"AttributeName": "GSI1SK", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GSI1",
                    "KeySchema": [
                        {"AttributeName": "GSI1PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table


class TestUserRepository:
    """ユーザーリポジトリのテスト"""

    def test_ユーザー保存_正常系(self, dynamodb_table):
        """ユーザーが正常に保存されること"""
        # Given: 有効なユーザー
        user = User.create(name="田中太郎", email="tanaka@example.com")
        repo = UserRepository(table=dynamodb_table)

        # When: 保存を実行
        repo.save(user)

        # Then: DynamoDBに保存される
        response = dynamodb_table.get_item(
            Key={"PK": f"USER#{user.user_id}", "SK": "PROFILE"}
        )
        assert response["Item"]["name"] == "田中太郎"

    def test_ユーザーID検索_存在する場合(self, dynamodb_table):
        """存在するユーザーIDで検索した場合にユーザーが返却されること"""
        # Given: 保存済みのユーザー
        user = User.create(name="田中太郎", email="tanaka@example.com")
        repo = UserRepository(table=dynamodb_table)
        repo.save(user)

        # When: IDで検索
        result = repo.find_by_id(user.user_id)

        # Then: ユーザーが返却される
        assert result is not None
        assert result.name == "田中太郎"

    def test_ユーザーID検索_存在しない場合(self, dynamodb_table):
        """存在しないユーザーIDで検索した場合にNoneが返却されること"""
        # Given: 空のテーブル
        repo = UserRepository(table=dynamodb_table)

        # When: 存在しないIDで検索
        result = repo.find_by_id("nonexistent-id")

        # Then: Noneが返却される
        assert result is None
