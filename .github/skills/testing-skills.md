# テストスキル定義

## pytest 基本パターン

### Given-When-Then 形式

```python
def test_ユーザー作成_正常系():
    """正しい入力でユーザーが作成されること"""
    # Given: 有効なユーザーデータ
    user_data = {"name": "田中太郎", "email": "tanaka@example.com"}

    # When: ユーザー作成を実行
    result = create_user(user_data)

    # Then: ユーザーが正常に作成される
    assert result.name == "田中太郎"
    assert result.email == "tanaka@example.com"
    assert result.user_id is not None
```

### フィクスチャの活用

```python
import pytest

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
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table
```

### パラメタライズドテスト

```python
@pytest.mark.parametrize(
    "email, expected_valid",
    [
        ("user@example.com", True),
        ("invalid-email", False),
        ("", False),
        ("user@.com", False),
    ],
)
def test_メールアドレスバリデーション(email, expected_valid):
    """各種メールアドレスのバリデーション結果を検証"""
    if expected_valid:
        user = User(name="テスト", email=email)
        assert user.email == email
    else:
        with pytest.raises(ValidationError):
            User(name="テスト", email=email)
```

## moto によるAWSモック

### DynamoDB モック

```python
from moto import mock_dynamodb

@mock_dynamodb
def test_ユーザー保存():
    """DynamoDBにユーザーが保存されること"""
    # テーブルセットアップ
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    table = dynamodb.create_table(...)

    # テスト実行
    repo = UserRepository(table)
    repo.save(User(user_id="123", name="田中太郎", email="tanaka@example.com"))

    # 検証
    response = table.get_item(Key={"PK": "USER#123", "SK": "PROFILE"})
    assert response["Item"]["name"] == "田中太郎"
```

### EventBridge モック

```python
from moto import mock_events

@mock_events
def test_ユーザー作成イベント発行():
    """ユーザー作成時にイベントが発行されること"""
    client = boto3.client("events", region_name="ap-northeast-1")
    # テスト実行・検証
```
