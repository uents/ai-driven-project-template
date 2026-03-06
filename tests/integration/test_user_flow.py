"""統合テスト: ユーザー作成フロー"""

import json

import boto3
import pytest
from moto import mock_dynamodb


@pytest.fixture
def setup_dynamodb():
    """統合テスト用DynamoDBテーブルのセットアップ"""
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        table = dynamodb.create_table(
            TableName="my-app-table",
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


class TestUserCreationFlow:
    """ユーザー作成フローの統合テスト"""

    def test_ユーザー作成から取得までの一連のフロー(self, setup_dynamodb):
        """ユーザーを作成し、その後取得できることを検証する"""
        # TODO: 統合テストの実装
        pass

    def test_メールアドレス重複時のエラーフロー(self, setup_dynamodb):
        """同じメールアドレスで2回ユーザー作成した場合のエラーを検証する"""
        # TODO: 統合テストの実装
        pass
