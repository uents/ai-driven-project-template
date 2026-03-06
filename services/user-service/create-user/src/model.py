"""ユーザードメインモデル"""

import json
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, field_validator


class CreateUserRequest(BaseModel):
    """ユーザー作成リクエスト"""

    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """ユーザー名のバリデーション"""
        if len(v) < 2:
            raise ValueError("ユーザー名は2文字以上で入力してください")
        if len(v) > 50:
            raise ValueError("ユーザー名は50文字以下で入力してください")
        return v


class User(BaseModel):
    """ユーザードメインモデル"""

    user_id: str
    name: str
    email: EmailStr
    created_at: str
    updated_at: str

    @classmethod
    def create(cls, name: str, email: str) -> "User":
        """新規ユーザーを作成する"""
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            user_id=str(uuid.uuid4()),
            name=name,
            email=email,
            created_at=now,
            updated_at=now,
        )

    def to_dynamodb_item(self) -> dict:
        """DynamoDB用のアイテムに変換する"""
        return {
            "PK": f"USER#{self.user_id}",
            "SK": "PROFILE",
            "GSI1PK": f"EMAIL#{self.email}",
            "GSI1SK": f"USER#{self.user_id}",
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "User":
        """DynamoDBアイテムからユーザーを復元する"""
        return cls(
            user_id=item["user_id"],
            name=item["name"],
            email=item["email"],
            created_at=item["created_at"],
            updated_at=item["updated_at"],
        )

    def to_json(self) -> str:
        """JSON文字列に変換する"""
        return json.dumps(
            {
                "user_id": self.user_id,
                "name": self.name,
                "email": self.email,
                "created_at": self.created_at,
            }
        )
