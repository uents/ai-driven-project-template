"""ユーザーリポジトリ"""

import os

import boto3
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key

from model import User

logger = Logger(child=True)

# テーブル名は環境変数から取得
TABLE_NAME = os.environ.get("TABLE_NAME", "my-app-table")


class UserRepository:
    """ユーザーデータへのアクセスを提供するリポジトリ"""

    def __init__(self, table=None):
        """リポジトリを初期化する

        Args:
            table: DynamoDBテーブルリソース（テスト時にモックを注入可能）
        """
        if table is None:
            dynamodb = boto3.resource("dynamodb")
            self.table = dynamodb.Table(TABLE_NAME)
        else:
            self.table = table

    def save(self, user: User) -> None:
        """ユーザーを保存する

        Args:
            user: 保存するユーザーオブジェクト
        """
        logger.info("ユーザーを保存します", extra={"user_id": user.user_id})
        self.table.put_item(Item=user.to_dynamodb_item())

    def find_by_id(self, user_id: str) -> User | None:
        """ユーザーIDでユーザーを検索する

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかった場合はUserオブジェクト、見つからない場合はNone
        """
        logger.info("ユーザーを検索します", extra={"user_id": user_id})
        response = self.table.get_item(
            Key={"PK": f"USER#{user_id}", "SK": "PROFILE"}
        )
        item = response.get("Item")
        return User.from_dynamodb_item(item) if item else None

    def find_by_email(self, email: str) -> User | None:
        """メールアドレスでユーザーを検索する

        Args:
            email: 検索するメールアドレス

        Returns:
            見つかった場合はUserオブジェクト、見つからない場合はNone
        """
        logger.info("メールアドレスでユーザーを検索します", extra={"email": email})
        response = self.table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1PK").eq(f"EMAIL#{email}"),
        )
        items = response.get("Items", [])
        return User.from_dynamodb_item(items[0]) if items else None
