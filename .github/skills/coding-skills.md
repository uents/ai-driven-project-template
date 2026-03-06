# コーディングスキル定義

## レイヤード構造

本プロジェクトでは、各機能を以下のレイヤーで構成する。

### Handler（ハンドラー層）

- Lambda のエントリポイント
- リクエストのバリデーションとレスポンスの整形を担当
- ビジネスロジックは含めない

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

### Model（モデル層）

- ドメインモデルの定義
- Pydantic を使用してバリデーションを組み込む

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """ユーザードメインモデル"""
    user_id: str
    name: str
    email: EmailStr
```

### Repository（リポジトリ層）

- データの永続化を担当
- DynamoDB へのアクセスをカプセル化

```python
class UserRepository:
    """ユーザーリポジトリ"""

    def __init__(self, table):
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
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class NotFoundError(AppError):
    """リソースが見つからない場合のエラー"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource}が見つかりません: {resource_id}",
            error_code="NOT_FOUND",
        )

class ValidationError(AppError):
    """バリデーションエラー"""
    def __init__(self, message: str):
        super().__init__(message=message, error_code="VALIDATION_ERROR")
```
