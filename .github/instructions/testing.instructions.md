---
applyTo: "**/test_*.py,**/tests/**,tests/**"
---

# テスト 指示

## テスト方針

- すべての機能にはユニットテストを必ず作成すること
- テストは Given-When-Then パターンで記述すること
- テスト名は日本語で意図が分かるように命名すること（例: `test_ユーザー作成_正常系`）

## ユニットテスト

- 配置場所: `services/{サービス名}/{機能名}/src/tests/`
- 外部依存（DynamoDB, EventBridge等）はモックすること
- `moto` ライブラリを使用してAWSサービスをモックすること
- カバレッジ目標: 80%以上

### Given-When-Then パターン

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
import boto3
from moto import mock_aws

@pytest.fixture
def dynamodb_table():
    """テスト用DynamoDBテーブルのセットアップ"""
    with mock_aws():
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

### moto によるAWSモック

```python
from moto import mock_aws

@mock_aws
def test_ユーザー保存():
    """ユーザーがDynamoDBに保存されること"""
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    table = dynamodb.create_table(...)  # テーブルセットアップ

    repo = UserRepository(table)
    repo.save(User(user_id="123", name="田中太郎", email="tanaka@example.com"))

    response = table.get_item(Key={"PK": "USER#123", "SK": "PROFILE"})
    assert response["Item"]["name"] == "田中太郎"
```

## 統合テスト

- 配置場所: `tests/integration/`
- 複数サービス間の連携を検証すること
- テスト環境のセットアップ/クリーンアップを必ず行うこと

## E2Eテスト

- 配置場所: `tests/e2e/`
- 実際のAPIエンドポイントに対して実行すること
- テストデータは `tests/fixtures/` を参照すること

## テストデータ

- 共通テストデータは `tests/fixtures/` に配置すること
- テスト固有のデータはテストファイル内に定義すること
