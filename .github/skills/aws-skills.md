# AWSスキル定義

## Lambda Powertools for Python

### Logger

```python
from aws_lambda_powertools import Logger

logger = Logger(service="user-service")

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info("ユーザー作成処理を開始")
    # 処理
```

### Tracer

```python
from aws_lambda_powertools import Tracer

tracer = Tracer(service="user-service")

@tracer.capture_lambda_handler
def handler(event, context):
    return process(event)

@tracer.capture_method
def process(event):
    # 処理
```

### Metrics

```python
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit

metrics = Metrics(namespace="MyApp", service="user-service")

@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event, context):
    metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)
```

## DynamoDB操作パターン

### テーブル初期化

```python
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-table")
```

### アイテム取得（単一キー）

```python
response = table.get_item(Key={"PK": "USER#123", "SK": "PROFILE"})
item = response.get("Item")
```

### クエリ（パーティションキー指定）

```python
from boto3.dynamodb.conditions import Key

response = table.query(
    KeyConditionExpression=Key("PK").eq("USER#123") & Key("SK").begins_with("ORDER#")
)
items = response["Items"]
```

### アイテム作成

```python
table.put_item(
    Item={
        "PK": "USER#123",
        "SK": "PROFILE",
        "name": "田中太郎",
        "email": "tanaka@example.com",
    }
)
```

## EventBridge パターン

### イベント発行

```python
import json
import boto3

eventbridge = boto3.client("events")

eventbridge.put_events(
    Entries=[
        {
            "Source": "custom.user-service",
            "DetailType": "UserCreated",
            "Detail": json.dumps({"user_id": "123", "name": "田中太郎"}),
            "EventBusName": "default",
        }
    ]
)
```
