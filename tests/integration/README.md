# 統合テスト

## 概要

複数のサービス・コンポーネント間の連携を検証するテストです。

## テスト戦略

- AWSサービス間の連携（Lambda → DynamoDB → EventBridge）を検証する
- LocalStack または moto を使用してAWSサービスをシミュレートする
- テストデータは `tests/fixtures/` の共通データを使用する

## 実行方法

```bash
# 統合テストの実行
task test:integration

# 特定のテストファイルのみ実行
pytest tests/integration/test_user_flow.py -v
```

## 前提条件

- Python 3.13 がインストールされていること
- 必要なパッケージがインストールされていること（`pip install -r requirements-dev.txt`）
