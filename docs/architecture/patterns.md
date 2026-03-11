# 採用パターン・規約

## アーキテクチャパターン

### サーバーレスマイクロサービス

- 各機能を独立したLambda関数として実装する
- 機能間の依存は最小限にする
- 共有状態はDynamoDBを通じてのみアクセスする

### イベント駆動

- サービス間通信はEventBridgeを使用する
- 同期的なサービス間呼び出しは原則禁止
- イベントスキーマは `contracts/events/schemas/` で管理する

### Single Table Design

- DynamoDBは単一テーブルで複数エンティティを管理する
- PK/SKの設計パターン: `{エンティティ}#{ID}`
- アクセスパターンに基づいてGSIを設計する

## コード構成パターン

### 機能単位のディレクトリ構成

```
{機能名}/
  ├── __init__.py
  ├── docs/
  │   ├── design.md         # 機能設計書
  │   └── diagrams/
  │       └── *.pu          # 設計図（PlantUML形式）
  ├── src/
  │   ├── __init__.py
  │   ├── handler.py        # Lambdaハンドラー
  │   └── *.py
  └── tests/
      ├── __init__.py
      ├── test_*.py
      ├── conftest.py
      └── test.env
```

### レイヤー責務

| レイヤー   | 責務                             | 禁止事項             |
| ---------- | -------------------------------- | -------------------- |
| Handler    | リクエスト受付・レスポンス整形   | ビジネスロジック     |
| Model      | ドメインロジック・バリデーション | 外部サービスアクセス |
| Repository | データ永続化                     | ビジネスルール       |

### 実装コードパターン

#### Handler

```python
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()

@app.post("/users")
@tracer.capture_method
def create_user():
    body = app.current_event.json_body
    # バリデーション → サービス呼び出し → レスポンス整形
```

#### Model

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """ユーザードメインモデル"""
    user_id: str
    name: str
    email: EmailStr
```

#### Repository

```python
class UserRepository:
    """ユーザーリポジトリ"""

    def __init__(self, table) -> None:
        self.table = table

    def save(self, user: User) -> None:
        """ユーザーを保存する"""
        self.table.put_item(Item=user.to_dynamodb_item())

    def find_by_id(self, user_id: str) -> User | None:
        """ユーザーIDで検索する"""
        response = self.table.get_item(Key={"PK": f"USER#{user_id}", "SK": "PROFILE"})
        item = response.get("Item")
        return User.from_dynamodb_item(item) if item else None
```

## エラーハンドリングパターン

### カスタム例外の定義

```python
class AppError(Exception):
    """アプリケーションエラーの基底クラス"""
    def __init__(self, message: str, error_code: str) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class NotFoundError(AppError):
    """リソースが見つからない場合のエラー"""
    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(
            message=f"{resource}が見つかりません: {resource_id}",
            error_code="NOT_FOUND",
        )

class ValidationError(AppError):
    """バリデーションエラー"""
    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_code="VALIDATION_ERROR")
```
