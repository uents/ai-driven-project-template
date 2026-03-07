---
applyTo: "**/*.py,infra/**,**/*.ts"
---

# AWS 指示

## Lambda

- Lambda関数は必ず AWS Lambda Powertools for Python を使用すること
- Logger, Tracer, Metrics の3つを標準で組み込むこと
- ハンドラー関数には `@logger.inject_lambda_context` デコレータを付与すること
- コールドスタートを意識し、グローバルスコープでの初期化を活用すること

## DynamoDB

- boto3のDynamoDB Resourceではなく、Tableリソースを使用すること
- テーブル定義は `contracts/database/table-definitions.yml` を参照すること
- アクセスパターンは `contracts/database/access-patterns.md` を参照すること
- Single Table Design を採用しているため、PK/SKの設計パターンに従うこと

## EventBridge

- イベントスキーマは `contracts/events/schemas/` に定義されたJSON Schemaに準拠すること
- イベントソースは `custom.{サービス名}` の形式とすること

## CDK

- CDK のスタック定義は `infra/cdk/stacks/` 配下に配置すること
- L2 Construct を優先的に使用すること
- リソースの命名規則: `{プロジェクト名}-{環境}-{リソース名}`

## コードサンプル

### Lambda Powertools 実装パターン

```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger(service="user-service")
tracer = Tracer(service="user-service")
metrics = Metrics(namespace="MyApp", service="user-service")

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    logger.info("処理を開始")
    metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)
    return process(event)

@tracer.capture_method
def process(event):
    # ビジネスロジック
    pass
```

### DynamoDB 操作パターン

```python
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-table")

# アイテム取得
response = table.get_item(Key={"PK": "USER#123", "SK": "PROFILE"})
item = response.get("Item")

# クエリ
response = table.query(
    KeyConditionExpression=Key("PK").eq("USER#123") & Key("SK").begins_with("ORDER#")
)

# アイテム作成
table.put_item(Item={"PK": "USER#123", "SK": "PROFILE", "name": "田中太郎"})
```

### EventBridge 発行パターン

```python
import json
import boto3

eventbridge = boto3.client("events")
eventbridge.put_events(
    Entries=[{
        "Source": "custom.user-service",
        "DetailType": "UserCreated",
        "Detail": json.dumps({"user_id": "123"}),
        "EventBusName": "default",
    }]
)
```
